from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import LoginApi, LogoutApi, MeApi, RegisterApi

app_name = "authentication"

urlpatterns: list[URLPattern] = [
    path("login/", LoginApi.as_view(), name="auth-login"),
    path("logout/", LogoutApi.as_view(), name="auth-logout"),
    path("me/", MeApi.as_view(), name="user-details"),
    path("register/", RegisterApi.as_view(), name="user-register"),
]
