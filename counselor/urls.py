from django.urls import path

from . import views

app_name = "counselor"

urlpatterns = [
    path("", views.counselor_home, name="home"),
    path("students/<int:student_id>/", views.student_detail, name="student_detail"),
]

