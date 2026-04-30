from django.db import models
from django.conf import settings


class CareerRecommendation(models.Model):
    """AI-based career recommendation for a student."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    assessment_result = models.ForeignKey('assessments.AssessmentResult', on_delete=models.CASCADE, related_name='recommendations')
    recommended_career = models.CharField(max_length=200)
    confidence_score = models.FloatField(default=0.0)  # percentage match
    description = models.TextField()
    skills_required = models.TextField()  # comma separated skills
    roadmap = models.JSONField(default=list)  # list of steps
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-confidence_score']

    def __str__(self):
        return f"{self.student.username} → {self.recommended_career} ({self.confidence_score:.0f}%)"

    def get_skills_list(self):
        return [s.strip() for s in self.skills_required.split(',') if s.strip()]
