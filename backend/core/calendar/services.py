# calendars/services.py

from django.db import transaction

from core.users.models import User

from .models import Calendar


def calendar_create(user: User, *, name: str, description: str, color: str, is_visible: bool) -> Calendar:
    return Calendar.objects.create(
        user=user,
        name=name,
        description=description,
        color=color,
        is_visible=is_visible,
    )


@transaction.atomic
def calendar_update(calendar_id: str, user, *, name: str, description: str, color: str, is_visible: bool) -> Calendar:
    calendar = Calendar.objects.get(id=calendar_id, user=user)
    calendar.name = name
    calendar.description = description
    calendar.color = color
    calendar.is_visible = is_visible
    calendar.save()
    return calendar


def calendar_delete(calendar_id: str, user) -> None:
    Calendar.objects.filter(id=calendar_id, user=user).delete()
