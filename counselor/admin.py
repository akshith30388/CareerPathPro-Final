from django.contrib import admin

from .models import StudentNote


@admin.register(StudentNote)
class StudentNoteAdmin(admin.ModelAdmin):
    list_display = ("counselor", "student", "created_at", "updated_at")
    list_filter = ("created_at", "counselor")
    search_fields = ("counselor__username", "student__username", "note")

