from django.urls import path
from . import views

app_name = "engine"

urlpatterns = [
    path("", views.module_index, name="index"),
    path("action/<slug:slug>/<str:op>/", views.module_action, name="action"),
]
