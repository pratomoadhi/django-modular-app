from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("", views.landing, name="landing"),  # /product/
    path("create/", views.product_create, name="create"),
    path("edit/<int:pk>/", views.product_edit, name="edit"),
    path("delete/<int:pk>/", views.product_delete, name="delete"),
]
