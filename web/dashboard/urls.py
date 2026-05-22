from django.urls import path

from .views import dashboard, refresh_feed

app_name = "dashboard"
urlpatterns = [
    path("", dashboard, name="index"),
    path("refresh", refresh_feed, name="refresh"),
]
