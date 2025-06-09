from django.db.models import QuerySet

from core.events.models import Event


def get_event_by_id(event_id: str) -> Event:
    return Event.objects.select_related("calendar", "recurrence").get(id=event_id)


def get_user_events(user) -> QuerySet[Event]:
    return Event.objects.filter(user=user).select_related("calendar", "recurrence").order_by("-start_time")
