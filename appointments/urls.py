from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book_appointment, name='book'),
    path('my/', views.my_appointments, name='my_appointments'),
    path('manage/', views.manage_appointments, name='manage'),
    path('update/<int:pk>/', views.update_appointment, name='update'),
    path('feedback/<int:appointment_pk>/', views.give_feedback, name='feedback'),
]

