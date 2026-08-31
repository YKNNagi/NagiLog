from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create, name="create"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("update/<int:pk>/", views.update, name="update"),
]