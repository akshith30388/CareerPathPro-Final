from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from appointments.models import Appointment, Feedback
from assessments.models import AssessmentResult
from chat.models import Message
from recommendations.models import CareerRecommendation
from users.models import CounselorProfile, CustomUser, StudentProfile

from .forms import ResumeForm
from .models import Resume


def _display_name(user):
    return user.get_full_name() or user.username


def _student_metrics(user):
    assessments = AssessmentResult.objects.filter(student=user)
    appointments = Appointment.objects.filter(student=user).select_related('counselor')
    recommendations = CareerRecommendation.objects.filter(student=user)

    latest_result = assessments.first()
    top_recommendations = recommendations.order_by('-confidence_score', '-generated_at')[:3]
    recent_appointments = appointments.order_by('-date', '-created_at')[:5]

    return {
        'latest_result': latest_result,
        'top_recommendations': top_recommendations,
        'recent_appointments': recent_appointments,
        'total_assessments': assessments.count(),
        'total_recommendations': recommendations.count(),
        'pending_appointments': appointments.filter(status='pending').count(),
        'confirmed_appointments': appointments.filter(status='confirmed').count(),
        'unread_messages': Message.objects.filter(receiver=user, is_read=False).count(),
    }


def _counselor_metrics(user):
    appointments = Appointment.objects.filter(counselor=user).select_related('student')
    feedbacks = Feedback.objects.filter(counselor=user).select_related('student')

    total_appointments = appointments.count()
    pending = appointments.filter(status='pending').order_by('date', 'time_slot')
    confirmed = appointments.filter(status='confirmed')
    completed_count = appointments.filter(status='completed').count()
    avg_rating = feedbacks.aggregate(avg=Avg('rating'))['avg'] or 0

    completion_rate = round((completed_count / total_appointments) * 100, 1) if total_appointments else 0

    return {
        'pending': pending,
        'total_appointments': total_appointments,
        'pending_count': pending.count(),
        'confirmed_count': confirmed.count(),
        'completed_count': completed_count,
        'feedbacks': feedbacks.order_by('-created_at')[:5],
        'avg_rating': round(avg_rating, 1),
        'unread_messages': Message.objects.filter(receiver=user, is_read=False).count(),
        'students_helped': appointments.values('student').distinct().count(),
        'completion_rate': completion_rate,
    }


@login_required
def dashboard_redirect(request):
    """Redirect user to their appropriate dashboard."""
    user = request.user
    if user.role == 'admin' or user.is_staff:
        return redirect('dashboard:admin')
    if user.role == 'counselor':
        return redirect('dashboard:counselor')
    return redirect('dashboard:student')


@login_required
def student_dashboard(request):
    """Student dashboard with overview stats."""
    if not request.user.is_student():
        return redirect('dashboard:redirect')

    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    metrics = _student_metrics(request.user)

    context = {
        'profile': profile,
        'total_assessments': metrics['total_assessments'],
        'total_recommendations': metrics['total_recommendations'],
        'latest_result': metrics['latest_result'],
        'appointments': metrics['recent_appointments'],
        'pending_appointments': metrics['pending_appointments'],
        'confirmed_appointments': metrics['confirmed_appointments'],
        'recommendations': metrics['top_recommendations'],
        'unread_messages': metrics['unread_messages'],
    }
    return render(request, 'dashboard/student.html', context)


@login_required
def student_dashboard_data(request):
    """Live JSON data for student dashboard widgets."""
    if not request.user.is_student():
        return JsonResponse({'detail': 'Forbidden'}, status=403)

    metrics = _student_metrics(request.user)

    latest_result = metrics['latest_result']
    latest_payload = None
    if latest_result:
        latest_payload = {
            'score': latest_result.score,
            'total_questions': latest_result.total_questions,
            'percentage': round(latest_result.percentage, 1),
            'taken_at': latest_result.taken_at.strftime('%b %d, %Y'),
            'result_url': reverse('assessments:result', args=[latest_result.pk]),
        }

    appointments_payload = [
        {
            'id': apt.pk,
            'counselor_name': _display_name(apt.counselor),
            'date': apt.date.strftime('%b %d, %Y'),
            'time': apt.get_time_slot_display(),
            'status': apt.status,
            'status_display': apt.get_status_display(),
        }
        for apt in metrics['recent_appointments']
    ]

    recommendations_payload = [
        {
            'id': rec.pk,
            'career': rec.recommended_career,
            'confidence': round(rec.confidence_score, 1),
        }
        for rec in metrics['top_recommendations']
    ]

    return JsonResponse({
        'totals': {
            'assessments': metrics['total_assessments'],
            'recommendations': metrics['total_recommendations'],
            'confirmed_sessions': metrics['confirmed_appointments'],
            'unread_messages': metrics['unread_messages'],
        },
        'latest_result': latest_payload,
        'appointments': appointments_payload,
        'recommendations': recommendations_payload,
        'updated_at': timezone.localtime().strftime('%I:%M %p'),
    })


@login_required
def counselor_dashboard(request):
    """Counselor dashboard."""
    if not request.user.is_counselor():
        return redirect('dashboard:redirect')

    profile, _ = CounselorProfile.objects.get_or_create(user=request.user)
    metrics = _counselor_metrics(request.user)

    context = {
        'profile': profile,
        'total_appointments': metrics['total_appointments'],
        'pending_appointments': metrics['pending'],
        'pending_appointments_count': metrics['pending_count'],
        'confirmed_appointments': metrics['confirmed_count'],
        'completed_appointments': metrics['completed_count'],
        'feedbacks': metrics['feedbacks'],
        'avg_rating': metrics['avg_rating'],
        'unread_messages': metrics['unread_messages'],
        'students_helped': metrics['students_helped'],
        'completion_rate': metrics['completion_rate'],
    }
    return render(request, 'dashboard/counselor.html', context)


@login_required
def counselor_dashboard_data(request):
    """Live JSON data for counselor dashboard widgets."""
    if not request.user.is_counselor():
        return JsonResponse({'detail': 'Forbidden'}, status=403)

    metrics = _counselor_metrics(request.user)

    pending_payload = [
        {
            'id': apt.pk,
            'student_name': _display_name(apt.student),
            'date': apt.date.strftime('%b %d, %Y'),
            'time': apt.get_time_slot_display(),
            'notes': apt.notes,
            'confirm_url': reverse('appointments:update', args=[apt.pk]),
        }
        for apt in metrics['pending'][:8]
    ]

    feedback_payload = [
        {
            'student_name': _display_name(item.student),
            'rating': item.rating,
            'comment': item.comment,
        }
        for item in metrics['feedbacks']
    ]

    return JsonResponse({
        'totals': {
            'pending': metrics['pending_count'],
            'confirmed': metrics['confirmed_count'],
            'completed': metrics['completed_count'],
            'unread_messages': metrics['unread_messages'],
            'students_helped': metrics['students_helped'],
            'completion_rate': metrics['completion_rate'],
            'total_appointments': metrics['total_appointments'],
            'avg_rating': metrics['avg_rating'],
        },
        'pending_appointments': pending_payload,
        'recent_feedbacks': feedback_payload,
        'updated_at': timezone.localtime().strftime('%I:%M %p'),
    })


@login_required
def admin_dashboard(request):
    """Admin dashboard with analytics."""
    if not (request.user.role == 'admin' or request.user.is_staff):
        return redirect('dashboard:redirect')

    total_students = CustomUser.objects.filter(role='student').count()
    total_counselors = CustomUser.objects.filter(role='counselor').count()
    total_appointments = Appointment.objects.count()
    total_assessments = AssessmentResult.objects.count()

    top_careers = (
        CareerRecommendation.objects.values('recommended_career')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    appointment_stats = {
        'pending': Appointment.objects.filter(status='pending').count(),
        'confirmed': Appointment.objects.filter(status='confirmed').count(),
        'completed': Appointment.objects.filter(status='completed').count(),
        'cancelled': Appointment.objects.filter(status='cancelled').count(),
    }

    recent_students = CustomUser.objects.filter(role='student').order_by('-date_joined')[:10]
    recent_appointments = Appointment.objects.order_by('-created_at')[:10]
    avg_feedback = Feedback.objects.aggregate(avg=Avg('rating'))['avg'] or 0

    context = {
        'total_students': total_students,
        'total_counselors': total_counselors,
        'total_appointments': total_appointments,
        'total_assessments': total_assessments,
        'top_careers': top_careers,
        'appointment_stats': appointment_stats,
        'recent_students': recent_students,
        'recent_appointments': recent_appointments,
        'avg_feedback': round(avg_feedback, 1),
    }
    return render(request, 'dashboard/admin.html', context)


@login_required
def resume_builder(request):
    """Build and save resume."""
    if not request.user.is_student():
        messages.error(request, 'Only students can build resumes.')
        return redirect('dashboard:redirect')

    resume, _ = Resume.objects.get_or_create(
        student=request.user,
        defaults={
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        },
    )

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            resume = form.save()

            edu_list = []
            edu_degrees = request.POST.getlist('edu_degree')
            edu_institutions = request.POST.getlist('edu_institution')
            edu_years = request.POST.getlist('edu_year')
            edu_grades = request.POST.getlist('edu_grade')
            for i, degree in enumerate(edu_degrees):
                if degree:
                    edu_list.append({
                        'degree': degree,
                        'institution': edu_institutions[i] if i < len(edu_institutions) else '',
                        'year': edu_years[i] if i < len(edu_years) else '',
                        'grade': edu_grades[i] if i < len(edu_grades) else '',
                    })
            resume.education = edu_list

            exp_list = []
            exp_titles = request.POST.getlist('exp_title')
            exp_companies = request.POST.getlist('exp_company')
            exp_durations = request.POST.getlist('exp_duration')
            exp_descs = request.POST.getlist('exp_desc')
            for i, title in enumerate(exp_titles):
                if title:
                    exp_list.append({
                        'title': title,
                        'company': exp_companies[i] if i < len(exp_companies) else '',
                        'duration': exp_durations[i] if i < len(exp_durations) else '',
                        'description': exp_descs[i] if i < len(exp_descs) else '',
                    })
            resume.experience = exp_list
            resume.save()

            messages.success(request, 'Resume saved successfully!')
            return redirect('dashboard:resume_preview')
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'dashboard/resume_builder.html', {'form': form, 'resume': resume})


@login_required
def resume_preview(request):
    """Preview the generated resume."""
    resume = get_object_or_404(Resume, student=request.user)
    return render(request, 'dashboard/resume_preview.html', {'resume': resume})
