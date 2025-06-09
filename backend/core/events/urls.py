from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import EventCreateApi, EventDeleteApi, EventDetailApi, EventListApi, EventUpdateApi

app_name = "events"

urlpatterns: list[URLPattern] = [
    path("", EventListApi.as_view(), name="event-list"),
    path("create/", EventCreateApi.as_view(), name="event-create"),
    path("<uuid:event_id>/", EventDetailApi.as_view(), name="event-detail"),
    path("<uuid:event_id>/update/", EventUpdateApi.as_view(), name="event-update"),
    path("<uuid:event_id>/delete/", EventDeleteApi.as_view(), name="event-delete"),
]
