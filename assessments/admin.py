from django.contrib import admin
from .models import AssessmentQuestion, AssessmentResult


@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_text', 'category', 'correct_option', 'is_active', 'order']
    list_filter = ['category', 'is_active']
    list_editable = ['is_active', 'order', 'correct_option']
    search_fields = ['question_text']


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'score', 'total_questions', 'percentage', 'taken_at']
    list_filter = ['taken_at']
    search_fields = ['student__username']
    readonly_fields = ['taken_at']
