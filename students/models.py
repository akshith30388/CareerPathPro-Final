from django.conf import settings
from django.db import models


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ("single", "Single Choice"),
        ("multiple", "Multiple Choice"),
        ("text", "Text Answer"),
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="questions")
    topic = models.CharField(max_length=255)
    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default="single")
    marks = models.IntegerField(default=1)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.assignment.title}: {self.question_text[:60]}"


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text[:80]


class StudentSubmission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignment_submissions")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    submitted_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    total_score = models.FloatField(default=0)
    percentage = models.FloatField(default=0)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.student} - {self.assignment} ({'Submitted' if self.is_submitted else 'In Progress'})"


class StudentAnswer(models.Model):
    submission = models.ForeignKey(StudentSubmission, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="student_answers")
    selected_options = models.ManyToManyField(Option, blank=True)
    text_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.FloatField(default=0)

    class Meta:
        unique_together = ("submission", "question")

    def __str__(self):
        return f"Answer for {self.question_id} by {self.submission.student_id}"


class TopicAnalysis(models.Model):
    STRENGTH_CHOICES = [("strong", "Strong"), ("average", "Average"), ("weak", "Weak")]

    submission = models.ForeignKey(StudentSubmission, on_delete=models.CASCADE, related_name="topic_analyses")
    topic = models.CharField(max_length=255)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    score_percentage = models.FloatField(default=0)
    strength_level = models.CharField(max_length=10, choices=STRENGTH_CHOICES, default="average")

    class Meta:
        unique_together = ("submission", "topic")
        ordering = ["topic"]

    def __str__(self):
        return f"{self.topic} ({self.score_percentage:.1f}%)"


class CounselorAssignment(models.Model):
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_counselor_rel",
    )
    counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_students",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.student} -> {self.counselor}"

