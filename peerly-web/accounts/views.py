from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, EditProfileForm
from main.models import StudentProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please sign in to continue.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            is_first_login = user.last_login is None
            login(request, user)
            messages.success(request, f'Welcome back, {user.full_name}!')
            if is_first_login:
                request.session['needs_onboarding'] = True
                return redirect('onboarding-step1')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('landing-page')


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})


@login_required
def profile_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'profile': profile,
    })


@login_required
def edit_profile_view(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            request.user.full_name = form.cleaned_data['full_name']
            request.user.save(update_fields=['full_name'])

            profile.degree = form.cleaned_data['degree']
            profile.year = form.cleaned_data['year']
            profile.bio = form.cleaned_data['bio']
            raw_interests = form.cleaned_data['interests']
            profile.interests = [i.strip() for i in raw_interests.split(',') if i.strip()] if raw_interests else []
            profile.birthday = form.cleaned_data['birthday']
            profile.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = EditProfileForm(initial={
            'full_name': request.user.full_name,
            'degree': profile.degree,
            'year': profile.year,
            'bio': profile.bio,
            'interests': ', '.join(profile.interests) if profile.interests else '',
            'birthday': profile.birthday,
        })

    return render(request, 'accounts/edit_profile.html', {
        'user': request.user,
        'profile': profile,
        'form': form,
    })

