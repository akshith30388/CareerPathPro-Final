from django.db import models
from django.conf import settings


class Resume(models.Model):
    """Student resume data."""
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resume')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=300, blank=True)
    summary = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    education = models.JSONField(default=list)   # [{degree, institution, year, grade}]
    experience = models.JSONField(default=list)  # [{title, company, duration, description}]
    languages = models.CharField(max_length=300, blank=True)
    hobbies = models.CharField(max_length=300, blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume: {self.student.username}"

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]
