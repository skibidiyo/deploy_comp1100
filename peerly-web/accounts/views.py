from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import Profile


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
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'interests': ['Ethical AI', 'Full Stack', 'Philosophy of Mind', 'Cybersecurity', 'UX Design'],
            'connections': 142,
            'active_groups': 8,
            'achievements': [
                {'title': 'Top Mentor', 'subtitle': 'CSSE1001'},
                {'title': 'Hackathon Winner', 'subtitle': 'UQ Hack 2023'},
                {'title': 'Peer Tutor', 'subtitle': 'Silver Tier'},
                {'title': "Dean's List", 'subtitle': 'S2 2023'},
            ],
            'recommended_buddies': [
                {'name': 'Sarah Jenkins', 'detail': 'Shared: PHIL1002'},
                {'name': "Liam O'Connor", 'detail': 'Shared: CSSE1001'},
            ],
            'timetable_summary': [
                {'day': 'MON', 'time': '10:00 AM - 12:00 PM', 'event': 'CSSE1001 - Lecture', 'location': 'Hawken Eng Building'},
                {'day': 'TUE', 'time': '02:00 PM - 03:00 PM', 'event': 'PHIL1002 - Tutorial', 'location': 'Forgan Smith'},
            ],
        }
    )
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'profile': profile,
    })

