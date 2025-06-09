from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import CalendarCreateApi, CalendarDeleteApi, CalendarDetailApi, CalendarListApi, CalendarUpdateApi

app_name = "calendar"

urlpatterns: list[URLPattern] = [
    path("", CalendarListApi.as_view(), name="calendar-list"),
    path("create/", CalendarCreateApi.as_view(), name="calendar-create"),
    path("<uuid:calendar_id>/", CalendarDetailApi.as_view(), name="calendar-detail"),
    path("<uuid:calendar_id>/update/", CalendarUpdateApi.as_view(), name="calendar-update"),
    path("<uuid:calendar_id>/delete/", CalendarDeleteApi.as_view(), name="calendar-delete"),
]
