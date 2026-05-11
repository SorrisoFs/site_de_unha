from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    Professional, Service, DateSlot, TimeSlot, Client, Scheduling
)


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'specialty']
    actions = ['activate_professionals', 'deactivate_professionals']

    @admin.action(description='Activate selected professionals')
    def activate_professionals(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected professionals')
    def deactivate_professionals(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_minutes', 'price', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 0
    fields = ['start_time', 'end_time', 'status']
    ordering = ['start_time']


@admin.register(DateSlot)
class DateSlotAdmin(admin.ModelAdmin):
    list_display = ['date', 'professional', 'is_available', 'slot_count', 'booked_count']
    list_filter = ['date', 'professional', 'is_available']
    search_fields = ['professional__name']
    inlines = [TimeSlotInline]
    actions = ['open_scheduling', 'close_scheduling']

    @admin.display(description='Total Slots')
    def slot_count(self, obj):
        return obj.time_slots.count()

    @admin.display(description='Booked')
    def booked_count(self, obj):
        return obj.time_slots.filter(status='booked').count()

    @admin.action(description='Open scheduling for selected dates')
    def open_scheduling(self, request, queryset):
        queryset.update(is_available=True)

    @admin.action(description='Close scheduling for selected dates')
    def close_scheduling(self, request, queryset):
        queryset.update(is_available=False)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['date_slot', 'start_time', 'end_time', 'status', 'scheduling_info']
    list_filter = ['status', 'date_slot__date', 'date_slot__professional']
    search_fields = ['date_slot__professional__name']

    @admin.display(description='Booking')
    def scheduling_info(self, obj):
        if hasattr(obj, 'scheduling'):
            client = obj.scheduling.client
            return format_html(
                '<a href="{}">{}</a> - {}',
                reverse('admin:scheduling_scheduling_change', args=[obj.scheduling.id]),
                client.name,
                client.phone
            )
        return '-'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['booking_token_short', 'name', 'phone', 'email', 'scheduling_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'phone', 'email', 'booking_token']
    readonly_fields = ['booking_token', 'created_at']

    @admin.display(description='Token')
    def booking_token_short(self, obj):
        return obj.booking_token[:8]

    @admin.display(description='Bookings')
    def scheduling_count(self, obj):
        return obj.schedulings.count()


@admin.register(Scheduling)
class SchedulingAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_info', 'service', 'time_slot_info', 'status', 'booked_at']
    list_filter = ['status', 'service', 'booked_at', 'time_slot__date_slot__date']
    search_fields = ['client__name', 'client__phone', 'client__booking_token']
    readonly_fields = ['booked_at', 'updated_at']
    actions = ['confirm_schedulings', 'cancel_schedulings', 'mark_completed']

    @admin.display(description='Client')
    def client_info(self, obj):
        return f"{obj.client.name} ({obj.client.phone})"

    @admin.display(description='Appointment')
    def time_slot_info(self, obj):
        ds = obj.time_slot.date_slot
        return f"{ds.date} {obj.time_slot.start_time.strftime('%H:%M')} - {ds.professional.name}"

    @admin.action(description='Confirm selected bookings')
    def confirm_schedulings(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Cancel selected bookings')
    def cancel_schedulings(self, request, queryset):
        queryset.update(status='cancelled')

    @admin.action(description='Mark as completed')
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')