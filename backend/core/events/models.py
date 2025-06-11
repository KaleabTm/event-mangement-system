from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from core.calendar.models import Calendar
from core.common.models import BaseModel

User = get_user_model()


class RecurrenceRule(BaseModel):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    WEEKDAY = "WEEKDAY"
    DATE = "DATE"

    FREQUENCY_CHOICES = [
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (MONTHLY, "Monthly"),
        (YEARLY, "Yearly"),
    ]

    MONTHLY_TYPE = [
        (WEEKDAY, "Weekday"),
        (DATE, "Date"),
    ]

    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    monthly_type = models.CharField(max_length=10, choices=MONTHLY_TYPE, blank=True, null=True)
    interval = models.PositiveIntegerField(default=1)
    weekdays = models.JSONField(blank=True, null=True)
    weekday_ordinal = models.IntegerField(blank=True, null=True)
    end_date = models.DateField(null=True, blank=True)
    repeat_count = models.PositiveIntegerField(null=True, blank=True)

    def clean(self):
        super().clean()
        if self.weekdays is not None:
            if not isinstance(self.weekdays, list) or not all(isinstance(i, int) for i in self.weekdays):
                raise ValidationError({"weekdays": "weekdays must be a list of integers."})
        if not (1 <= self.interval <= 365):
            raise ValidationError({"interval": "Interval must be between 1 and 365."})


class Event(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    color = models.CharField(max_length=7, null=True, blank=True)
    recurrence = models.OneToOneField(
        RecurrenceRule,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="event",
    )
    is_all_day = models.BooleanField(default=False)

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def __str__(self):
        return f"{self.title} - {self.user.email} ({self.start_time} to {self.end_time})"

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
