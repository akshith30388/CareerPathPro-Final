from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AssessmentQuestion, AssessmentResult
from .forms import AssessmentAnswerForm
from recommendations.engine import generate_recommendations


@login_required
def assessment_start(request):
    """Show assessment start page."""
    questions = AssessmentQuestion.objects.filter(is_active=True)
    already_taken = AssessmentResult.objects.filter(student=request.user).first()
    return render(request, 'assessments/start.html', {
        'total_questions': questions.count(),
        'already_taken': already_taken,
    })


@login_required
def take_assessment(request):
    """Render and handle MCQ assessment form."""
    if not request.user.is_student():
        messages.error(request, 'Only students can take assessments.')
        return redirect('dashboard:redirect')

    # Check if user explicitly clicked "Retake" button
    is_retake = request.GET.get('retake', 'false').lower() == 'true'
    
    # If not a retake attempt and user has existing results, redirect to last result
    if not is_retake:
        last_result = AssessmentResult.objects.filter(student=request.user).first()
        if last_result and request.method != 'POST':
            return redirect('assessments:result', pk=last_result.pk)

    questions = list(AssessmentQuestion.objects.filter(is_active=True))

    if not questions:
        messages.warning(request, 'No assessment questions available. Please ask an admin to add questions.')
        return redirect('assessments:start')

    if request.method == 'POST':
        form = AssessmentAnswerForm(request.POST, questions=questions)
        if form.is_valid():
            answers = {}
            score = 0
            career_scores = {}

            for q in questions:
                selected = form.cleaned_data.get(f'question_{q.id}')
                if selected:
                    answers[str(q.id)] = selected
                    # Score correct answers
                    if selected == q.correct_option:
                        score += 1
                    # Map answer to career interest
                    career_map = {
                        'a': q.option_a_career,
                        'b': q.option_b_career,
                        'c': q.option_c_career,
                        'd': q.option_d_career,
                    }
                    career = career_map.get(selected, '')
                    if career:
                        career_scores[career] = career_scores.get(career, 0) + 1

            total = len(questions)
            percentage = (score / total * 100) if total > 0 else 0

            result = AssessmentResult.objects.create(
                student=request.user,
                score=score,
                total_questions=total,
                percentage=percentage,
                answers=answers,
                career_scores=career_scores,
            )

            # Generate recommendations
            generate_recommendations(request.user, result)

            messages.success(request, f'Assessment completed! You scored {score}/{total}.')
            return redirect('assessments:result', pk=result.pk)
        else:
            messages.error(request, 'Please answer all questions.')
    else:
        form = AssessmentAnswerForm(questions=questions)

    return render(request, 'assessments/take.html', {'form': form, 'questions': questions})


@login_required
def assessment_result(request, pk):
    """Show assessment result."""
    result = get_object_or_404(AssessmentResult, pk=pk, student=request.user)
    recommendations = result.recommendations.all()
    return render(request, 'assessments/result.html', {
        'result': result,
        'recommendations': recommendations,
    })


@login_required
def my_results(request):
    """List all assessment results for student."""
    results = AssessmentResult.objects.filter(student=request.user)
    return render(request, 'assessments/my_results.html', {'results': results})
