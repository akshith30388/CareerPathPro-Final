from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("assignments/", views.assignment_list, name="assignment_list"),
    path("assignments/<int:assignment_id>/start/", views.assignment_start, name="assignment_start"),
    path("assignments/<int:assignment_id>/take/", views.assignment_take, name="assignment_take"),
    path("assignments/<int:assignment_id>/submit/", views.assignment_submit, name="assignment_submit"),
    path("assignments/<int:assignment_id>/result/", views.assignment_result, name="assignment_result"),
    path("select-counselor/<int:counselor_id>/", views.select_counselor, name="select_counselor"),
]

