from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils import timezone
from django.views.decorators.http import require_POST, require_http_methods
import json

from .models import StudentProfile, Classmate, Course


def _format_date_label(current_date):
	day = current_date.day
	if 11 <= day % 100 <= 13:
		suffix = 'th'
	else:
		suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
	return current_date.strftime(f'%A, %B {day}{suffix}')


def _initials_for_name(full_name):
	parts = [part for part in full_name.split() if part]
	if not parts:
		return 'P'
	if len(parts) == 1:
		return parts[0][:2].upper()
	return f'{parts[0][0]}{parts[-1][0]}'.upper()

def landing_page(request):
	if request.user.is_authenticated:
		return redirect('home')
	return render(request, 'main/landing.html')

def _redirect_if_onboarding_not_needed(request):
	if not request.user.is_authenticated:
		return redirect('login')
	if not request.session.get('needs_onboarding'):
		return redirect('home')
	return None

@login_required
def onboarding_step1(request):
	redirect_response = _redirect_if_onboarding_not_needed(request)
	if redirect_response:
		return redirect_response
	return render(request, 'main/onboarding.html')

@login_required
def onboarding_step2(request):
	redirect_response = _redirect_if_onboarding_not_needed(request)
	if redirect_response:
		return redirect_response
	return render(request, 'main/onboarding_step2.html')

@login_required
def onboarding_step3(request):
	redirect_response = _redirect_if_onboarding_not_needed(request)
	if redirect_response:
		return redirect_response
	return render(request, 'main/onboarding_step3.html')

@login_required
def onboarding_step4(request):
	redirect_response = _redirect_if_onboarding_not_needed(request)
	if redirect_response:
		return redirect_response
	return render(request, 'main/onboarding_step4.html')

@login_required
def onboarding_step5(request):
	redirect_response = _redirect_if_onboarding_not_needed(request)
	if redirect_response:
		return redirect_response
	return render(request, 'main/onboarding_step5.html')

@login_required
def complete_onboarding(request):
	"""Complete onboarding and save StudentProfile to database"""
	if request.method == 'POST':
		# Get data from form submission (from localStorage)
		degree = request.POST.get('degree', '')
		year = request.POST.get('year', '')
		bio = request.POST.get('bio', '')
		interests_str = request.POST.get('interests', '')
		classes_str = request.POST.get('classes', '')
		
		# Parse interests and classes from comma-separated strings
		interests = [i.strip() for i in interests_str.split(',') if i.strip()] if interests_str else []
		classes = [c.strip() for c in classes_str.split(',') if c.strip()] if classes_str else []
		
		# Create or update StudentProfile
		try:
			profile = request.user.profile
		except StudentProfile.DoesNotExist:
			profile = StudentProfile(user=request.user)
		
		profile.degree = degree
		profile.year = year
		profile.bio = bio
		profile.interests = interests
		profile.classes = classes
		profile.save()
	
	request.session.pop('needs_onboarding', None)
	return redirect('home')

@login_required
def dashboard(request):
	"""Home/Discover page shown after login or onboarding completion"""
	return render(request, 'main/dashboard.html')

@login_required
def campus_events(request):
	return render(request, 'main/campus_events.html')


@login_required
@require_http_methods(["POST"])
def add_class(request):
	"""Add a class code to the user's StudentProfile"""
	try:
		# Get the class code from POST data
		class_code = request.POST.get('class_code', '').strip().upper()
		
		if not class_code:
			return JsonResponse({'success': False, 'message': 'Class code is required'}, status=400)
		
		# Get or create the user's StudentProfile
		try:
			profile = request.user.profile
		except StudentProfile.DoesNotExist:
			profile = StudentProfile(user=request.user)
		
		# Add class code if not already present
		if class_code not in profile.classes:
			profile.classes.append(class_code)
			profile.save()
			return JsonResponse({
				'success': True,
				'message': f'Added {class_code}',
				'class_code': class_code
			})
		else:
			return JsonResponse({
				'success': False,
				'message': f'{class_code} already added'
			}, status=400)
			
	except Exception as e:
		return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
def classmates_page(request):
	courses = Course.objects.all()
	selected_code = request.GET.get('course', '').strip().upper()
	selected_course = courses.filter(code=selected_code).first() if selected_code else courses.first()

	classmates = Classmate.objects.filter(course=selected_course) if selected_course else Classmate.objects.none()
	search_query = request.GET.get('q', '').strip()
	status_filter = request.GET.get('status', 'all').strip().lower()
	sort_by = request.GET.get('sort', 'recommended').strip().lower()

	if search_query:
		classmates = classmates.filter(
			Q(full_name__icontains=search_query) |
			Q(degree_name__icontains=search_query) |
			Q(course__code__icontains=search_query)
		)

	if status_filter in {Classmate.ActionState.CONNECT, Classmate.ActionState.GOING}:
		classmates = classmates.filter(action_state=status_filter)

	if sort_by == 'recent':
		classmates = classmates.order_by('-created_at', 'display_order', 'full_name')
	elif sort_by == 'name':
		classmates = classmates.order_by('full_name')
	elif sort_by == 'online':
		classmates = classmates.order_by('-is_online', 'display_order', 'full_name')
	else:
		classmates = classmates.order_by('display_order', 'full_name')

	current_user_name = request.user.get_full_name() or request.user.email.split('@')[0]
	context = {
		'courses': courses,
		'selected_course': selected_course,
		'classmates': classmates,
		'search_query': search_query,
		'status_filter': status_filter,
		'sort_by': sort_by,
		'today_label': _format_date_label(timezone.localdate()),
		'current_user_name': current_user_name,
		'current_user_initials': _initials_for_name(current_user_name),
	}
	return render(request, 'main/classmates.html', context)


@login_required
@require_POST
def toggle_classmate_status(request, classmate_id):
	classmate = get_object_or_404(Classmate, pk=classmate_id)
	classmate.action_state = (
		Classmate.ActionState.GOING
		if classmate.action_state == Classmate.ActionState.CONNECT
		else Classmate.ActionState.CONNECT
	)
	classmate.save(update_fields=['action_state'])

	next_url = request.POST.get('next') or reverse('classmates')
	if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
		next_url = reverse('classmates')
	return redirect(next_url)
