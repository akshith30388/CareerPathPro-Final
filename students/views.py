from collections import defaultdict
from datetime import timedelta

from asgiref.sync import async_to_sync
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from users.models import CustomUser

try:
    from channels.layers import get_channel_layer
except ImportError:
    def get_channel_layer():
        return None

from .models import (
    Assignment,
    CounselorAssignment,
    Question,
    StudentAnswer,
    StudentSubmission,
    TopicAnalysis,
)


def _require_student(request):
    if not request.user.is_student():
        messages.error(request, "Only students can access this page.")
        return False
    return True


def _active_submission(student, assignment):
    submission = StudentSubmission.objects.filter(
        student=student,
        assignment=assignment,
        is_submitted=False,
    ).first()
    if submission:
        return submission
    return StudentSubmission.objects.create(student=student, assignment=assignment)


def _save_answers(submission, payload):
    questions = list(
        submission.assignment.questions.prefetch_related("options").all()
    )
    errors = {}

    for question in questions:
        answer, _ = StudentAnswer.objects.get_or_create(submission=submission, question=question)
        key = f"question_{question.id}"
        answer.text_answer = ""
        answer.selected_options.clear()

        if question.question_type == "text":
            text_value = payload.get(key, "").strip()
            if not text_value:
                errors[key] = "This question is required."
            answer.text_answer = text_value
            answer.save()
            continue

        selected_ids = payload.getlist(key)
        if not selected_ids:
            errors[key] = "Please select at least one option."
            answer.save()
            continue

        valid_options = question.options.filter(id__in=selected_ids)
        answer.save()
        answer.selected_options.set(valid_options)

    return questions, errors


def _grade_submission(submission):
    answers = submission.answers.select_related("question").prefetch_related("selected_options", "question__options")
    topic_stats = defaultdict(lambda: {"correct": 0, "total": 0, "obtained": 0.0, "max_marks": 0.0})
    total_score = 0.0
    total_marks = 0.0

    for answer in answers:
        question = answer.question
        total_marks += question.marks

        if question.question_type in {"single", "multiple"}:
            selected_ids = set(answer.selected_options.values_list("id", flat=True))
            correct_ids = set(question.options.filter(is_correct=True).values_list("id", flat=True))
            is_correct = selected_ids == correct_ids and bool(correct_ids)
            marks_obtained = float(question.marks if is_correct else 0.0)
        else:
            is_correct = False
            marks_obtained = 0.0

        answer.is_correct = is_correct
        answer.marks_obtained = marks_obtained
        answer.save(update_fields=["is_correct", "marks_obtained"])

        total_score += marks_obtained
        topic_stats[question.topic]["total"] += 1
        topic_stats[question.topic]["max_marks"] += float(question.marks)
        topic_stats[question.topic]["obtained"] += marks_obtained
        if is_correct:
            topic_stats[question.topic]["correct"] += 1

    submission.total_score = total_score
    submission.percentage = (total_score / total_marks * 100) if total_marks else 0.0
    submission.is_submitted = True
    submission.completed_at = timezone.now()
    submission.save(update_fields=["total_score", "percentage", "is_submitted", "completed_at"])

    submission.topic_analyses.all().delete()
    analyses = []
    for topic, values in topic_stats.items():
        topic_percentage = (values["obtained"] / values["max_marks"] * 100) if values["max_marks"] else 0.0
        if topic_percentage >= 70:
            strength = "strong"
        elif topic_percentage >= 40:
            strength = "average"
        else:
            strength = "weak"
        analyses.append(
            TopicAnalysis(
                submission=submission,
                topic=topic,
                total_questions=values["total"],
                correct_answers=values["correct"],
                score_percentage=topic_percentage,
                strength_level=strength,
            )
        )

    TopicAnalysis.objects.bulk_create(analyses)
    return total_marks


def _grade_from_percentage(percentage):
    if percentage >= 90:
        return "A"
    if percentage >= 75:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 40:
        return "D"
    return "F"


def _suggestion(topic_analysis):
    if topic_analysis.strength_level == "weak":
        return f"Focus more on {topic_analysis.topic}. Revise fundamentals."
    if topic_analysis.strength_level == "average":
        return f"Good understanding of {topic_analysis.topic}. Practice more."
    return f"Excellent in {topic_analysis.topic}. Keep it up!"


def _broadcast_counselor_event(student, event_payload):
    assignment = CounselorAssignment.objects.filter(student=student, is_active=True).select_related("counselor").first()
    if not assignment:
        return
    channel_layer = get_channel_layer()
    if not channel_layer:
        return
    async_to_sync(channel_layer.group_send)(
        f"counselor_{assignment.counselor_id}",
        event_payload,
    )


@login_required
def assignment_list(request):
    if not _require_student(request):
        return redirect("dashboard:redirect")

    assignments = Assignment.objects.filter(is_active=True).prefetch_related("questions")
    submissions = {}
    for item in StudentSubmission.objects.filter(student=request.user).order_by("-submitted_at"):
        if item.assignment_id not in submissions:
            submissions[item.assignment_id] = item
    assignment_cards = [
        {"assignment": assignment, "submission": submissions.get(assignment.id)}
        for assignment in assignments
    ]
    return render(
        request,
        "student/assignments/list.html",
        {"assignment_cards": assignment_cards},
    )


@login_required
def assignment_start(request, assignment_id):
    if not _require_student(request):
        return redirect("dashboard:redirect")

    assignment = get_object_or_404(Assignment, id=assignment_id, is_active=True)
    _active_submission(request.user, assignment)
    return redirect("students:assignment_take", assignment_id=assignment.id)


@login_required
def assignment_take(request, assignment_id):
    if not _require_student(request):
        return redirect("dashboard:redirect")

    assignment = get_object_or_404(Assignment, id=assignment_id, is_active=True)
    submission = _active_submission(request.user, assignment)

    if request.method == "POST":
        _, errors = _save_answers(submission, request.POST)
        if errors:
            messages.error(request, "Please answer all required questions before continuing.")
        else:
            messages.success(request, "Answers saved successfully.")
            return redirect("students:assignment_take", assignment_id=assignment.id)

    questions = assignment.questions.prefetch_related("options").all()
    existing_answers = {
        answer.question_id: answer
        for answer in submission.answers.prefetch_related("selected_options").all()
    }
    question_payload = []
    for question in questions:
        answer = existing_answers.get(question.id)
        selected_ids = set(answer.selected_options.values_list("id", flat=True)) if answer else set()
        question_payload.append(
            {
                "question": question,
                "answer": answer,
                "selected_ids": selected_ids,
            }
        )
    return render(
        request,
        "student/assignments/take.html",
        {
            "assignment": assignment,
            "question_payload": question_payload,
            "submission": submission,
        },
    )


@login_required
def assignment_submit(request, assignment_id):
    if request.method != "POST":
        return redirect("students:assignment_take", assignment_id=assignment_id)

    if not _require_student(request):
        return redirect("dashboard:redirect")

    assignment = get_object_or_404(Assignment, id=assignment_id, is_active=True)
    submission = _active_submission(request.user, assignment)

    _, errors = _save_answers(submission, request.POST)
    if errors:
        messages.error(request, "Please answer all required questions before submitting.")
        return redirect("students:assignment_take", assignment_id=assignment.id)

    total_marks = _grade_submission(submission)
    _broadcast_counselor_event(
        request.user,
        {
            "type": "assignment_submitted",
            "student_id": request.user.id,
            "student_name": request.user.get_full_name() or request.user.username,
            "score": submission.total_score,
            "percentage": submission.percentage,
            "assignment_title": assignment.title,
            "submitted_at": timezone.localtime(submission.completed_at).isoformat(),
        },
    )

    messages.success(
        request,
        f"Assignment submitted successfully. Score: {submission.total_score:.1f}/{total_marks:.1f}",
    )
    return redirect("students:assignment_result", assignment_id=assignment.id)


@login_required
def assignment_result(request, assignment_id):
    if not _require_student(request):
        return redirect("dashboard:redirect")

    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission = (
        StudentSubmission.objects.filter(
            assignment=assignment,
            student=request.user,
            is_submitted=True,
        )
        .prefetch_related(
            "answers__selected_options",
            "answers__question__options",
            "topic_analyses",
        )
        .order_by("-completed_at")
        .first()
    )
    if not submission:
        messages.error(request, "No submitted result found for this assignment.")
        return redirect("students:assignment_list")

    total_marks = sum(question.marks for question in assignment.questions.all())
    grade = _grade_from_percentage(submission.percentage)
    duration = timedelta(0)
    if submission.completed_at:
        duration = submission.completed_at - submission.submitted_at

    topic_analyses = list(submission.topic_analyses.all())
    review_items = []
    for answer in submission.answers.select_related("question").prefetch_related("selected_options", "question__options"):
        question = answer.question
        correct_options = list(question.options.filter(is_correct=True).values_list("option_text", flat=True))
        selected_options = list(answer.selected_options.values_list("option_text", flat=True))
        review_items.append(
            {
                "question": question,
                "answer": answer,
                "selected_options": selected_options,
                "correct_options": correct_options,
            }
        )

    return render(
        request,
        "student/assignments/result.html",
        {
            "assignment": assignment,
            "submission": submission,
            "grade": grade,
            "total_marks": total_marks,
            "time_taken": duration,
            "topic_analyses": topic_analyses,
            "review_items": review_items,
            "topic_suggestions": {analysis.topic: _suggestion(analysis) for analysis in topic_analyses},
        },
    )


@login_required
def select_counselor(request, counselor_id):
    if request.method != "POST":
        return redirect("dashboard:student")

    if not _require_student(request):
        return redirect("dashboard:redirect")

    counselor = get_object_or_404(CustomUser, id=counselor_id, role="counselor")
    assignment, _ = CounselorAssignment.objects.update_or_create(
        student=request.user,
        defaults={"counselor": counselor, "is_active": True},
    )

    _broadcast_counselor_event(
        request.user,
        {
            "type": "student_assigned",
            "student_id": request.user.id,
            "student_name": request.user.get_full_name() or request.user.username,
            "assigned_at": timezone.localtime(assignment.assigned_at).isoformat(),
        },
    )
    messages.success(request, f"You are now connected with counselor {counselor.get_full_name() or counselor.username}.")
    return redirect(request.META.get("HTTP_REFERER") or "dashboard:student")
