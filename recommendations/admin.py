from django.contrib import admin
from .models import CareerRecommendation


@admin.register(CareerRecommendation)
class CareerRecommendationAdmin(admin.ModelAdmin):
    list_display = ['student', 'recommended_career', 'confidence_score', 'generated_at']
    list_filter = ['recommended_career', 'generated_at']
    search_fields = ['student__username', 'recommended_career']
    ordering = ['-confidence_score']
