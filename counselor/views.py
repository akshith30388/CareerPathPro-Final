from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from students.models import CounselorAssignment, StudentSubmission, TopicAnalysis
from users.models import CustomUser, StudentProfile

from .models import StudentNote


def _require_counselor(request):
    if not request.user.is_counselor():
        messages.error(request, "Only counselors can access this page.")
        return False
    return True


@login_required
def counselor_home(request):
    if not _require_counselor(request):
        return redirect("dashboard:redirect")
    return redirect("dashboard:counselor")


@login_required
def student_detail(request, student_id):
    if not _require_counselor(request):
        return redirect("dashboard:redirect")

    student = get_object_or_404(CustomUser, id=student_id, role="student")
    is_assigned = CounselorAssignment.objects.filter(
        student=student,
        counselor=request.user,
        is_active=True,
    ).exists()
    if not is_assigned:
        messages.error(request, "You are not assigned to this student.")
        return redirect("dashboard:counselor")

    if request.method == "POST":
        note_text = request.POST.get("note", "").strip()
        if note_text:
            StudentNote.objects.create(counselor=request.user, student=student, note=note_text)
            messages.success(request, "Note added successfully.")
            return redirect("counselor:student_detail", student_id=student.id)
        messages.error(request, "Note cannot be empty.")

    profile = StudentProfile.objects.filter(user=student).first()
    submissions = (
        StudentSubmission.objects.filter(student=student, is_submitted=True)
        .select_related("assignment")
        .order_by("-completed_at")
    )
    topic_analysis = TopicAnalysis.objects.filter(submission__student=student, submission__is_submitted=True)
    notes = StudentNote.objects.filter(student=student, counselor=request.user)

    return render(
        request,
        "counselor/student_detail.html",
        {
            "student_user": student,
            "profile": profile,
            "submissions": submissions,
            "topic_analysis": topic_analysis,
            "notes": notes,
        },
    )

