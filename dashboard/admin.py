from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['student', 'full_name', 'email', 'updated_at']
    search_fields = ['student__username', 'full_name', 'email']
