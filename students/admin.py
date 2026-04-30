from django.contrib import admin

from .models import (
    Assignment,
    CounselorAssignment,
    Option,
    Question,
    StudentAnswer,
    StudentSubmission,
    TopicAnalysis,
)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at", "due_date")
    list_filter = ("is_active", "created_at", "due_date")
    search_fields = ("title", "description")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "assignment", "topic", "question_type", "marks")
    list_filter = ("assignment", "question_type", "topic")
    search_fields = ("question_text", "topic", "assignment__title")


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "option_text", "is_correct")
    list_filter = ("is_correct", "question__assignment")
    search_fields = ("option_text", "question__question_text")


@admin.register(StudentSubmission)
class StudentSubmissionAdmin(admin.ModelAdmin):
    list_display = ("student", "assignment", "is_submitted", "total_score", "percentage", "submitted_at", "completed_at")
    list_filter = ("is_submitted", "assignment", "submitted_at")
    search_fields = ("student__username", "student__first_name", "assignment__title")


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ("submission", "question", "is_correct", "marks_obtained")
    list_filter = ("is_correct", "question__topic", "question__assignment")
    search_fields = ("question__question_text", "submission__student__username", "text_answer")


@admin.register(TopicAnalysis)
class TopicAnalysisAdmin(admin.ModelAdmin):
    list_display = ("submission", "topic", "total_questions", "correct_answers", "score_percentage", "strength_level")
    list_filter = ("strength_level", "topic")
    search_fields = ("topic", "submission__student__username", "submission__assignment__title")


@admin.register(CounselorAssignment)
class CounselorAssignmentAdmin(admin.ModelAdmin):
    list_display = ("student", "counselor", "assigned_at", "is_active")
    list_filter = ("is_active", "assigned_at")
    search_fields = ("student__username", "counselor__username")

