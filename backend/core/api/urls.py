from django.urls import include, path
from django.urls.resolvers import URLResolver

urlpatterns: list[URLResolver] = [
    path("auth/", include(("core.authentication.urls", "authentication"), namespace="authentication")),
    path("events/", include(("core.events.urls", "events"), namespace="events")),
    path("calendars/", include(("core.calendar.urls", "calendar"), namespace="calendar")),
]
