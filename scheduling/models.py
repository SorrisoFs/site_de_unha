import uuid
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone


class Professional(models.Model):
    """Professional who performs services."""
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    specialty = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    """Types of services offered (e.g., manicure, pedicure, nail art)."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.duration_minutes} min)"


class DateSlot(models.Model):
    """Represents a date when slots are available."""
    date = models.DateField()
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        related_name='date_slots'
    )
    is_available = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['date', 'professional']

    def __str__(self):
        return f"{self.date} - {self.professional.name}"


class TimeSlot(models.Model):
    """Individual time slots within a DateSlot."""
    SLOT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('blocked', 'Blocked by Admin'),
    ]

    date_slot = models.ForeignKey(
        DateSlot,
        on_delete=models.CASCADE,
        related_name='time_slots'
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=SLOT_STATUS_CHOICES,
        default='available'
    )

    class Meta:
        ordering = ['start_time']
        unique_together = ['date_slot', 'start_time']

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

    @property
    def is_bookable(self):
        return self.status == 'available' and self.date_slot.is_available


class Client(models.Model):
    """Client with minimal data for privacy."""
    booking_token = models.CharField(
        max_length=32,
        unique=True,
        default=uuid.uuid4().hex
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Client {self.booking_token[:8]}"

    def save(self, *args, **kwargs):
        if not self.booking_token:
            self.booking_token = uuid.uuid4().hex
        super().save(*args, **kwargs)


class Scheduling(models.Model):
    """Booking/Appointment model."""
    SCHEDULING_STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    time_slot = models.OneToOneField(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='scheduling'
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='schedulings'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='schedulings'
    )
    status = models.CharField(
        max_length=20,
        choices=SCHEDULING_STATUS_CHOICES,
        default='confirmed'
    )
    notes = models.TextField(blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.client} - {self.service.name} at {self.time_slot}"