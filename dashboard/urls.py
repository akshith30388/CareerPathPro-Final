from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_redirect, name='redirect'),
    path('student/', views.student_dashboard, name='student'),
    path('student/data/', views.student_dashboard_data, name='student_data'),
    path('counselor/', views.counselor_dashboard, name='counselor'),
    path('counselor/data/', views.counselor_dashboard_data, name='counselor_data'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('resume/builder/', views.resume_builder, name='resume_builder'),
    path('resume/preview/', views.resume_preview, name='resume_preview'),
]
