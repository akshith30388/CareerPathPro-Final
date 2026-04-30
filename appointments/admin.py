from django.contrib import admin
from .models import Appointment, Feedback


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'counselor', 'date', 'time_slot', 'status', 'created_at']
    list_filter = ['status', 'date']
    search_fields = ['student__username', 'counselor__username']
    list_editable = ['status']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['student', 'counselor', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['student__username', 'counselor__username']
