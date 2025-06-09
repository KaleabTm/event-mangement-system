from typing import Optional

from django.db import transaction

from core.calendar.models import Calendar
from core.users.models import User

from .models import Event, RecurrenceRule


def event_create(
    *,
    user: User,
    calendar: Calendar,
    title: str,
    description: str,
    start_time,
    end_time,
    color: Optional[str],
    is_all_day: bool,
    frequency: Optional[str] = None,
    interval: Optional[int] = None,
    weekdays: Optional[list] = None,
    weekday_ordinal: Optional[int] = None,
    end_date=None,
    repeat_count: Optional[int] = None,
) -> Event:
    with transaction.atomic():
        recurrence_obj = RecurrenceRule.objects.create(
            end_date=end_date,
            frequency=frequency,
            interval=interval,
            weekdays=weekdays,
            weekday_ordinal=weekday_ordinal,
            repeat_count=repeat_count,
        )

        return Event.objects.create(
            user=user,
            calendar=calendar,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            color=color,
            is_all_day=is_all_day,
            recurrence=recurrence_obj,
        )


def event_update(
    *,
    event: Event,
    calendar: Calendar,
    title: str,
    description: str,
    start_time,
    end_time,
    color: Optional[str],
    is_all_day: bool,
    frequency: Optional[str] = None,
    interval: Optional[int] = None,
    weekdays: Optional[list] = None,
    weekday_ordinal: Optional[int] = None,
    end_date=None,
    repeat_count: Optional[int] = None,
) -> Event:
    with transaction.atomic():
        has_recurrence_data = any([
            frequency,
            interval,
            weekdays,
            weekday_ordinal,
            end_date,
            repeat_count,
        ])

        if has_recurrence_data:
            recurrence_data = {
                "frequency": frequency,
                "interval": interval,
                "weekdays": weekdays,
                "weekday_ordinal": weekday_ordinal,
                "end_date": end_date,
                "repeat_count": repeat_count,
            }

            # Clean out keys with None to avoid unnecessary overwrites
            recurrence_data = {k: v for k, v in recurrence_data.items() if v is not None}

            if event.recurrence:
                for key, value in recurrence_data.items():
                    setattr(event.recurrence, key, value)
                event.recurrence.save()
            else:
                event.recurrence = RecurrenceRule.objects.create(**recurrence_data)

        elif event.recurrence:
            # Remove recurrence if no recurrence data is sent
            event.recurrence.delete()
            event.recurrence = None

        event.calendar = calendar
        event.title = title
        event.description = description
        event.start_time = start_time
        event.end_time = end_time
        event.color = color
        event.is_all_day = is_all_day

        event.save()

    return event


def event_delete(*, event: Event):
    event.delete()
