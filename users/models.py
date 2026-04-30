from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model with role field."""
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('counselor', 'Counselor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_student(self):
        return self.role == 'student'

    def is_counselor(self):
        return self.role == 'counselor'

    def is_admin_user(self):
        return self.role == 'admin'


class StudentProfile(models.Model):
    """Extended profile for students."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    bio = models.TextField(blank=True)
    interests = models.CharField(max_length=500, blank=True, help_text="Comma-separated interests")
    education_level = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Student Profile: {self.user.username}"


class CounselorProfile(models.Model):
    """Extended profile for counselors."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='counselor_profile')
    specialization = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    available_days = models.CharField(max_length=200, blank=True, help_text="e.g. Mon,Tue,Wed")
    qualification = models.CharField(max_length=200, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Counselor Profile: {self.user.username}"
