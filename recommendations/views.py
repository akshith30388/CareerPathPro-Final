from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CareerRecommendation
from assessments.models import AssessmentResult
from .engine import generate_recommendations


@login_required
def recommendation_list(request):
    """List all career recommendations for a student."""
    if not request.user.is_student():
        messages.error(request, 'Only students can view recommendations.')
        return redirect('dashboard:redirect')
    recommendations = CareerRecommendation.objects.filter(student=request.user)
    return render(request, 'recommendations/list.html', {'recommendations': recommendations})


@login_required
def recommendation_detail(request, pk):
    """Detailed view of a career recommendation with roadmap."""
    rec = get_object_or_404(CareerRecommendation, pk=pk, student=request.user)
    return render(request, 'recommendations/detail.html', {'rec': rec})


@login_required
def generate_from_result(request, result_pk):
    """Regenerate recommendations from an assessment result."""
    result = get_object_or_404(AssessmentResult, pk=result_pk, student=request.user)
    generate_recommendations(request.user, result)
    messages.success(request, 'Recommendations regenerated!')
    return redirect('recommendations:list')
