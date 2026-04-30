from django.db import models
from django.conf import settings


class AssessmentQuestion(models.Model):
    """MCQ question for career assessments."""
    CATEGORY_CHOICES = (
        ('aptitude', 'Aptitude'),
        ('interest', 'Interest'),
        ('personality', 'Personality'),
    )
    question_text = models.TextField()
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300)
    option_d = models.CharField(max_length=300)
    correct_option = models.CharField(max_length=1, choices=[('a','A'),('b','B'),('c','C'),('d','D')])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='aptitude')
    # Points for each option mapping to career interests
    option_a_career = models.CharField(max_length=100, blank=True)
    option_b_career = models.CharField(max_length=100, blank=True)
    option_c_career = models.CharField(max_length=100, blank=True)
    option_d_career = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Q{self.id}: {self.question_text[:60]}"


class AssessmentResult(models.Model):
    """Stores results of a student's assessment attempt."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assessment_results')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    taken_at = models.DateTimeField(auto_now_add=True)
    # Store answers as JSON: {question_id: selected_option}
    answers = models.JSONField(default=dict)
    # Career score mapping
    career_scores = models.JSONField(default=dict)

    class Meta:
        ordering = ['-taken_at']

    def __str__(self):
        return f"{self.student.username} - Score: {self.score}/{self.total_questions} on {self.taken_at.strftime('%Y-%m-%d')}"
