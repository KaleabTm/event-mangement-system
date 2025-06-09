# calendars/selectors.py

from django.db.models import QuerySet

from .models import Calendar


def get_all_calendars_for_user(user) -> QuerySet:
    return Calendar.objects.filter(user=user)


def get_calendar_by_id_for_user(calendar_id: str, user) -> Calendar:
    return Calendar.objects.get(id=calendar_id, user=user)
