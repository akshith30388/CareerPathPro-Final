from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Feedback
from .forms import BookAppointmentForm, FeedbackForm


@login_required
def book_appointment(request):
    """Book a new appointment."""
    if not request.user.is_student():
        messages.error(request, 'Only students can book appointments.')
        return redirect('dashboard:redirect')
    if request.method == 'POST':
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.student = request.user
            appointment.save()
            messages.success(request, 'Appointment booked successfully! Awaiting counselor confirmation.')
            return redirect('appointments:my_appointments')
    else:
        form = BookAppointmentForm()
    return render(request, 'appointments/book.html', {'form': form})


@login_required
def my_appointments(request):
    """List student's appointments."""
    appointments = Appointment.objects.filter(student=request.user)
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})


@login_required
def manage_appointments(request):
    """Counselor manages their appointments."""
    if not request.user.is_counselor():
        messages.error(request, 'Only counselors can manage appointments.')
        return redirect('dashboard:redirect')
    appointments = Appointment.objects.filter(counselor=request.user)
    return render(request, 'appointments/manage.html', {'appointments': appointments})


@login_required
def update_appointment(request, pk):
    """Counselor confirms or cancels an appointment."""
    appointment = get_object_or_404(Appointment, pk=pk, counselor=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')
        counselor_notes = request.POST.get('counselor_notes', '')
        if status in ['confirmed', 'cancelled', 'completed']:
            appointment.status = status
            appointment.counselor_notes = counselor_notes
            appointment.save()
            messages.success(request, f'Appointment {status} successfully.')
    return redirect('appointments:manage')


@login_required
def give_feedback(request, appointment_pk):
    """Student gives feedback after completed appointment."""
    appointment = get_object_or_404(Appointment, pk=appointment_pk, student=request.user, status='completed')
    # Check if feedback already given
    if hasattr(appointment, 'feedback'):
        messages.info(request, 'You have already given feedback for this appointment.')
        return redirect('appointments:my_appointments')
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.appointment = appointment
            feedback.student = request.user
            feedback.counselor = appointment.counselor
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('appointments:my_appointments')
    else:
        form = FeedbackForm()
    return render(request, 'appointments/feedback.html', {'form': form, 'appointment': appointment})
