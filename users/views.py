from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import CustomUser, StudentProfile, CounselorProfile
from .forms import RegisterForm, LoginForm, StudentProfileForm, CounselorProfileForm


def home_view(request):
    """Landing page."""
    return render(request, 'home.html')


def register_view(request):
    """User registration with role selection."""
    if request.user.is_authenticated:
        return redirect('dashboard:redirect')
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                # Create profile based on role
                if user.role == 'student':
                    StudentProfile.objects.create(user=user)
                elif user.role == 'counselor':
                    CounselorProfile.objects.create(user=user)
                login(request, user)
                messages.success(request, f'Welcome, {user.get_full_name() or user.username}! Account created successfully.')
                return redirect('dashboard:redirect')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('dashboard:redirect')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                next_url = request.GET.get('next', '')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard:redirect')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Logout and redirect to login."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login')


@login_required
def student_dashboard(request):
    """Student-specific dashboard."""
    if not request.user.is_student():
        messages.error(request, 'Access denied.')
        return redirect('dashboard:redirect')
    return redirect('dashboard:student')


@login_required
def counselor_dashboard(request):
    """Counselor-specific dashboard."""
    if not request.user.is_counselor():
        messages.error(request, 'Access denied.')
        return redirect('dashboard:redirect')
    return redirect('dashboard:counselor')


@login_required
def profile_view(request):
    """View user profile."""
    user = request.user
    profile = None
    if user.is_student():
        profile, _ = StudentProfile.objects.get_or_create(user=user)
    elif user.is_counselor():
        profile, _ = CounselorProfile.objects.get_or_create(user=user)
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def edit_profile_view(request):
    """Edit user profile."""
    user = request.user
    if user.is_student():
        profile, _ = StudentProfile.objects.get_or_create(user=user)
        form_class = StudentProfileForm
    elif user.is_counselor():
        profile, _ = CounselorProfile.objects.get_or_create(user=user)
        form_class = CounselorProfileForm
    else:
        messages.error(request, 'Profile editing not available for admin.')
        return redirect('dashboard:admin')

    if request.method == 'POST':
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # Update user fields
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.phone = request.POST.get('phone', user.phone)
            if request.FILES.get('profile_picture'):
                user.profile_picture = request.FILES['profile_picture']
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
    else:
        form = form_class(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form, 'profile': profile})
