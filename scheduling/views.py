from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
import uuid

from .models import (
    Professional, Service, DateSlot, TimeSlot, Client, Scheduling
)
from .forms import DateSlotForm, QuickScheduleForm


# =============================================================================
# CLIENT VIEWS (Public - No Authentication Required)
# =============================================================================

def home(request):
    """Home page with calendar and services."""
    services = Service.objects.filter(is_active=True)
    professionals = Professional.objects.filter(is_active=True)

    today = datetime.now().date()
    # Get available dates (dates that have at least one available slot)
    available_dates = DateSlot.objects.filter(
        is_available=True,
        date__gte=today,
        time_slots__status='available'
    ).values_list('date', flat=True).distinct()

    available_dates_json = [d.isoformat() for d in available_dates]

    return render(request, 'scheduling/home.html', {
        'services': services,
        'professionals': professionals,
        'available_dates_json': available_dates_json,
    })


@require_http_methods(["GET", "POST"])
def book_service(request):
    """
    Simple booking form with just name and phone.
    Date and time are selected via calendar.
    """
    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_slot_id = request.POST.get('time_slot_id')
        client_name = request.POST.get('client_name', '').strip()
        client_phone = request.POST.get('client_phone', '').strip()
        service_id = request.POST.get('service')

        errors = []

        if not client_name:
            errors.append('Nome completo é obrigatório.')
        if not client_phone:
            errors.append('Celular é obrigatório.')
        if not date_str:
            errors.append('Data é obrigatória.')
        if not time_slot_id:
            errors.append('Horário é obrigatório.')
        if not service_id:
            errors.append('Serviço é obrigatório.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        try:
            time_slot = TimeSlot.objects.get(id=time_slot_id)
            if not time_slot.is_bookable:
                return JsonResponse({'success': False, 'errors': ['Horário não disponível.']}, status=400)

            service = Service.objects.get(id=service_id)

            # Create or get client
            client, created = Client.objects.get_or_create(
                phone=client_phone,
                defaults={'name': client_name}
            )

            if not created:
                client.name = client_name
                client.save()

            # Create scheduling
            scheduling = Scheduling.objects.create(
                time_slot=time_slot,
                client=client,
                service=service
            )

            # Update time slot
            time_slot.status = 'booked'
            time_slot.save()

            return JsonResponse({
                'success': True,
                'booking_token': client.booking_token,
                'message': 'Agendamento realizado com sucesso!'
            })

        except (TimeSlot.DoesNotExist, Service.DoesNotExist) as e:
            return JsonResponse({'success': False, 'errors': ['Horário ou serviço inválido.']}, status=400)

    return JsonResponse({'success': False, 'errors': ['Método não permitido.']}, status=405)


def get_available_slots(request):
    """Get available time slots for a specific date (API)."""
    date_str = request.GET.get('date')
    professional_id = request.GET.get('professional')

    if not date_str:
        return JsonResponse({'error': 'Data obrigatória'}, status=400)

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Data inválida'}, status=400)

    date_slots = DateSlot.objects.filter(
        date=selected_date,
        is_available=True
    )

    if professional_id:
        date_slots = date_slots.filter(professional_id=professional_id)

    time_slots = TimeSlot.objects.filter(
        date_slot__in=date_slots,
        status='available'
    ).select_related('date_slot__professional').order_by('start_time')

    slots_data = [{
        'id': slot.id,
        'start_time': slot.start_time.strftime('%H:%M'),
        'end_time': slot.end_time.strftime('%H:%M'),
        'professional': slot.date_slot.professional.name
    } for slot in time_slots]

    return JsonResponse({'slots': slots_data})


def available_slots(request):
    """View available time slots for booking."""
    date_str = request.GET.get('date')
    professional_id = request.GET.get('professional')
    service_id = request.GET.get('service')

    context = {
        'selected_date': date_str,
        'selected_professional_id': professional_id,
        'selected_service_id': service_id,
    }

    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'scheduling/available_slots.html', context)

        date_slots = DateSlot.objects.filter(
            date=selected_date,
            is_available=True
        )

        if professional_id:
            date_slots = date_slots.filter(professional_id=professional_id)

        time_slots = TimeSlot.objects.filter(
            date_slot__in=date_slots,
            status='available'
        ).select_related('date_slot', 'date_slot__professional').order_by('start_time')

        context['time_slots'] = time_slots
        context['date_slot'] = date_slots.first()

    context['services'] = Service.objects.filter(is_active=True)
    context['professionals'] = Professional.objects.filter(is_active=True)

    return render(request, 'scheduling/available_slots.html', context)


def check_booking(request):
    """Allow clients to check their booking using booking token."""
    token = request.GET.get('token')

    if token:
        try:
            client = Client.objects.get(booking_token=token)
            schedulings = client.schedulings.filter(
                time_slot__date_slot__date__gte=timezone.now().date()
            ).select_related(
                'time_slot__date_slot__professional', 'service'
            ).order_by('time_slot__date_slot__date', 'time_slot__start_time')

            return render(request, 'scheduling/my_bookings.html', {
                'schedulings': schedulings,
                'client': client,
            })
        except Client.DoesNotExist:
            return render(request, 'scheduling/check_booking.html', {
                'error': 'Código de agendamento não encontrado.'
            })

    return render(request, 'scheduling/check_booking.html')


@require_http_methods(["POST"])
def cancel_booking(request):
    """Cancel a booking using booking token."""
    token = request.POST.get('token')
    scheduling_id = request.POST.get('scheduling_id')

    if not token or not scheduling_id:
        return JsonResponse({'success': False, 'error': 'Dados incompletos.'})

    try:
        client = Client.objects.get(booking_token=token)
        scheduling = client.schedulings.get(id=scheduling_id)

        if scheduling.status != 'cancelled':
            scheduling.status = 'cancelled'
            scheduling.save()

            scheduling.time_slot.status = 'available'
            scheduling.time_slot.save()

        return JsonResponse({'success': True})
    except (Client.DoesNotExist, Scheduling.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Agendamento não encontrado.'})


# =============================================================================
# ADMIN VIEWS (Authentication Required)
# =============================================================================

@staff_member_required
def admin_dashboard(request):
    """Admin dashboard with overview statistics."""
    today = timezone.now().date()

    context = {
        'total_schedulings_today': Scheduling.objects.filter(
            time_slot__date_slot__date=today
        ).count(),
        'upcoming_schedulings': Scheduling.objects.filter(
            time_slot__date_slot__date__gte=today,
            status='confirmed'
        ).count(),
        'total_clients': Client.objects.count(),
        'recent_schedulings': Scheduling.objects.select_related(
            'client', 'service', 'time_slot__date_slot__professional'
        ).order_by('-booked_at')[:10],
    }

    return render(request, 'scheduling/admin/dashboard.html', context)


@staff_member_required
def admin_scheduling_list(request):
    """List all schedulings with filtering."""
    status_filter = request.GET.get('status')
    date_filter = request.GET.get('date')

    schedulings = Scheduling.objects.select_related(
        'client', 'service', 'time_slot__date_slot__professional'
    )

    if status_filter:
        schedulings = schedulings.filter(status=status_filter)

    if date_filter:
        schedulings = schedulings.filter(time_slot__date_slot__date=date_filter)

    paginator = Paginator(schedulings, 25)
    page = request.GET.get('page')
    schedulings = paginator.get_page(page)

    return render(request, 'scheduling/admin/scheduling_list.html', {
        'schedulings': schedulings,
        'status_choices': Scheduling.SCHEDULING_STATUS_CHOICES,
    })


@staff_member_required
def admin_create_date_slot(request):
    """Create a date slot with auto-generated time slots."""
    if request.method == 'POST':
        form = DateSlotForm(request.POST)
        if form.is_valid():
            date_slot = form.save()
            return redirect('scheduling:admin_date_slot_detail', pk=date_slot.pk)
    else:
        form = DateSlotForm()

    return render(request, 'scheduling/admin/date_slot_form.html', {
        'form': form,
        'action': 'Create'
    })


@staff_member_required
def admin_date_slot_detail(request, pk):
    """View and manage time slots for a specific date."""
    date_slot = get_object_or_404(DateSlot, pk=pk)
    time_slots = date_slot.time_slots.all().select_related('scheduling__client')

    return render(request, 'scheduling/admin/date_slot_detail.html', {
        'date_slot': date_slot,
        'time_slots': time_slots,
    })


@staff_member_required
def admin_quick_schedule(request):
    """Admin quick scheduling - bypass normal flow."""
    if request.method == 'POST':
        form = QuickScheduleForm(request.POST)
        if form.is_valid():
            scheduling = form.save()
            return redirect('scheduling:admin_scheduling_list')
    else:
        form = QuickScheduleForm()

    return render(request, 'scheduling/admin/quick_schedule.html', {
        'form': form,
    })


@staff_member_required
def admin_block_time_slot(request, slot_id):
    """Block a specific time slot."""
    slot = get_object_or_404(TimeSlot, id=slot_id)
    slot.status = 'blocked'
    slot.save()
    return redirect('scheduling:admin_date_slot_detail', pk=slot.date_slot.pk)


@staff_member_required
def admin_unblock_time_slot(request, slot_id):
    """Unblock a time slot."""
    slot = get_object_or_404(TimeSlot, id=slot_id)
    slot.status = 'available'
    slot.save()
    return redirect('scheduling:admin_date_slot_detail', pk=slot.date_slot.pk)


@staff_member_required
def admin_client_list(request):
    """List all clients with their booking history."""
    search = request.GET.get('search')

    clients = Client.objects.all()

    if search:
        clients = clients.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(booking_token__icontains=search)
        )

    paginator = Paginator(clients, 30)
    page = request.GET.get('page')
    clients = paginator.get_page(page)

    return render(request, 'scheduling/admin/client_list.html', {
        'clients': clients,
    })


@staff_member_required
def admin_client_detail(request, pk):
    """View client details and booking history."""
    client = get_object_or_404(Client, pk=pk)
    schedulings = client.schedulings.select_related(
        'time_slot__date_slot__professional', 'service'
    ).order_by('-booked_at')

    return render(request, 'scheduling/admin/client_detail.html', {
        'client': client,
        'schedulings': schedulings,
    })


# =============================================================================
# API VIEWS (Return JSON for AJAX calls)
# =============================================================================

def api_available_slots(request):
    """API endpoint to get available slots as JSON."""
    date_str = request.GET.get('date')
    professional_id = request.GET.get('professional')

    if not date_str:
        return JsonResponse({'error': 'Date required'}, status=400)

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    date_slots = DateSlot.objects.filter(
        date=selected_date,
        is_available=True
    )

    if professional_id:
        date_slots = date_slots.filter(professional_id=professional_id)

    time_slots = TimeSlot.objects.filter(
        date_slot__in=date_slots,
        status='available'
    ).select_related('date_slot__professional')

    slots_data = [{
        'id': slot.id,
        'start_time': slot.start_time.strftime('%H:%M'),
        'end_time': slot.end_time.strftime('%H:%M'),
        'professional': slot.date_slot.professional.name
    } for slot in time_slots]

    return JsonResponse({'slots': slots_data})


def api_services_by_professional(request):
    """Get services that a professional can perform."""
    services = Service.objects.filter(is_active=True)

    services_data = [{
        'id': s.id,
        'name': s.name,
        'duration_minutes': s.duration_minutes,
        'price': str(s.price)
    } for s in services]

    return JsonResponse({'services': services_data})