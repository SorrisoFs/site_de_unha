from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Scheduling, TimeSlot, Client, Service, Professional, DateSlot


class BookingForm(forms.Form):
    """Form for clients to book an appointment."""

    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Serviço'
    )
    professional = forms.ModelChoiceField(
        queryset=Professional.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Profissional',
        required=False
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': timezone.now().date().isoformat()
        }),
        label='Data'
    )
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Horário'
    )
    client_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Seu Nome'
    )
    client_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999'
        }),
        label='Telefone'
    )
    client_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email (opcional)'
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label='Observações (opcional)'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        time_slot = cleaned_data.get('time_slot')

        if time_slot and not time_slot.is_bookable:
            raise ValidationError('Este horário não está mais disponível.')

        return cleaned_data

    def save(self):
        """Create client and scheduling."""
        cd = self.cleaned_data

        client, created = Client.objects.get_or_create(
            phone=cd['client_phone'],
            defaults={
                'name': cd['client_name'],
                'email': cd.get('client_email', ''),
            }
        )

        if not created:
            client.name = cd['client_name']
            client.email = cd.get('client_email', '') or client.email
            client.save()

        scheduling = Scheduling.objects.create(
            time_slot=cd['time_slot'],
            client=client,
            service=cd['service'],
            notes=cd.get('notes', '')
        )

        cd['time_slot'].status = 'booked'
        cd['time_slot'].save()

        return scheduling


class DateSlotForm(forms.ModelForm):
    """Form for admin to create date slots and auto-generate time slots."""

    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label='Horário de início'
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        label='Horário de término'
    )
    interval_minutes = forms.IntegerField(
        initial=30,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Intervalo entre horários (minutos)'
    )

    class Meta:
        model = DateSlot
        fields = ['date', 'professional', 'is_available', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'professional': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')

        if start and end and start >= end:
            raise ValidationError('Horário de início deve ser antes do término.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            self._create_time_slots(instance)

        return instance

    def _create_time_slots(self, date_slot):
        """Auto-generate time slots based on start, end, and interval."""
        start = self.cleaned_data['start_time']
        end = self.cleaned_data['end_time']
        interval = self.cleaned_data['interval_minutes']

        current = datetime.combine(date_slot.date, start)
        end_dt = datetime.combine(date_slot.date, end)

        slots_to_create = []
        while current < end_dt:
            slot_end = current + timedelta(minutes=interval)

            if slot_end <= end_dt:
                slots_to_create.append(TimeSlot(
                    date_slot=date_slot,
                    start_time=current.time(),
                    end_time=slot_end.time(),
                    status='available'
                ))

            current = slot_end

        if slots_to_create:
            TimeSlot.objects.bulk_create(slots_to_create, ignore_conflicts=True)


class QuickScheduleForm(forms.Form):
    """Quick scheduling form for admin."""

    client_name = forms.CharField(max_length=100)
    client_phone = forms.CharField(max_length=20)
    service = forms.ModelChoiceField(queryset=Service.objects.filter(is_active=True))
    time_slot = forms.ModelChoiceField(
        queryset=TimeSlot.objects.filter(status='available'),
        label='Horário'
    )
    notes = forms.CharField(required=False, widget=forms.Textarea)

    def save(self):
        cd = self.cleaned_data

        client, _ = Client.objects.get_or_create(
            phone=cd['client_phone'],
            defaults={'name': cd['client_name']}
        )

        scheduling = Scheduling.objects.create(
            time_slot=cd['time_slot'],
            client=client,
            service=cd['service'],
            notes=cd.get('notes', '')
        )

        cd['time_slot'].status = 'booked'
        cd['time_slot'].save()

        return scheduling