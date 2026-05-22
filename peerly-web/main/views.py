from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST, require_http_methods
import json

from accounts.models import PeerlyUser
from .models import StudentProfile, DiscoverAction, StudySession


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
		
		# Parse interests from comma-separated string
		interests = [i.strip() for i in interests_str.split(',') if i.strip()] if interests_str else []
		# Parse classes — handle both JSON array (from dashboard localStorage) and comma-separated
		try:
			parsed = json.loads(classes_str)
			classes = [str(c).strip() for c in parsed if str(c).strip()] if isinstance(parsed, list) else []
		except (json.JSONDecodeError, ValueError):
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

def _suggested_classmates(user, limit=5):
	try:
		user_classes = set(user.profile.classes or [])
	except StudentProfile.DoesNotExist:
		return []
	if not user_classes:
		return []
	already_seen = set(DiscoverAction.objects.filter(user=user).values_list('target_user_id', flat=True))
	results = []
	for profile in StudentProfile.objects.exclude(user=user).select_related('user'):
		if profile.user_id in already_seen:
			continue
		shared = sorted(user_classes & set(profile.classes or []))
		if not shared:
			continue
		name = profile.user.get_full_name() or profile.user.email.split('@')[0]
		results.append({
			'name': name,
			'initials': _initials_for_name(name),
			'shared_classes': shared,
			'gradient': _AVATAR_GRADIENTS[profile.user.id % len(_AVATAR_GRADIENTS)],
		})
		if len(results) >= limit:
			break
	return results


@login_required
def dashboard(request):
	current_user_name = request.user.get_full_name() or request.user.email.split('@')[0]
	try:
		user_classes = request.user.profile.classes or []
	except StudentProfile.DoesNotExist:
		user_classes = []

	upcoming_sessions = (
		StudySession.objects
		.filter(course_code__in=user_classes, scheduled_at__gte=timezone.now())
		.prefetch_related('attendees')[:3]
	) if user_classes else []

	return render(request, 'main/dashboard.html', {
		'current_user_name': current_user_name,
		'current_user_initials': _initials_for_name(current_user_name),
		'suggested_classmates': _suggested_classmates(request.user),
		'upcoming_sessions': upcoming_sessions,
		'user_classes': user_classes,
	})


@login_required
@require_POST
def create_study_session(request):
	try:
		data = json.loads(request.body)
		title = data.get('title', '').strip()
		course_code = data.get('course_code', '').strip().upper()
		location = data.get('location', '').strip()
		scheduled_at = data.get('scheduled_at', '').strip()

		if not title or not course_code or not scheduled_at:
			return JsonResponse({'success': False, 'message': 'Title, course, and date/time are required'}, status=400)

		from django.utils.dateparse import parse_datetime
		dt = parse_datetime(scheduled_at)
		if not dt:
			return JsonResponse({'success': False, 'message': 'Invalid date/time format'}, status=400)

		session = StudySession.objects.create(
			title=title,
			course_code=course_code,
			location=location,
			scheduled_at=dt,
			host=request.user,
		)
		session.attendees.add(request.user)
		return JsonResponse({'success': True, 'message': 'Study session created!', 'id': session.id})
	except Exception as e:
		return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
@require_POST
def toggle_study_session(request, session_id):
	session = get_object_or_404(StudySession, pk=session_id)
	if request.user in session.attendees.all():
		session.attendees.remove(request.user)
		joined = False
	else:
		session.attendees.add(request.user)
		joined = True
	return JsonResponse({'success': True, 'joined': joined, 'count': session.attendees.count()})

@login_required
def campus_events(request):
	current_user_name = request.user.get_full_name() or request.user.email.split('@')[0]
	return render(request, 'main/campus_events.html', {
		'current_user_name': current_user_name,
		'current_user_initials': _initials_for_name(current_user_name),
	})


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


_AVATAR_GRADIENTS = [
	'linear-gradient(135deg,#667eea,#764ba2)',
	'linear-gradient(135deg,#f093fb,#f5576c)',
	'linear-gradient(135deg,#4facfe,#00f2fe)',
	'linear-gradient(135deg,#43e97b,#38f9d7)',
	'linear-gradient(135deg,#fa709a,#fee140)',
	'linear-gradient(135deg,#a18cd1,#fbc2eb)',
	'linear-gradient(135deg,#fd7043,#ff8a65)',
	'linear-gradient(135deg,#26c6da,#00acc1)',
]


@login_required
def classmates_page(request):
	try:
		current_profile = request.user.profile
		user_classes = current_profile.classes or []
	except StudentProfile.DoesNotExist:
		user_classes = []

	selected_code = request.GET.get('course', '').strip().upper()
	if not selected_code and user_classes:
		selected_code = user_classes[0]

	search_query = request.GET.get('q', '').strip()
	sort_by = request.GET.get('sort', 'recommended').strip().lower()

	# Find real users who share the selected class
	peers = []
	if selected_code:
		other_profiles = StudentProfile.objects.exclude(user=request.user).select_related('user')
		for p in other_profiles:
			if selected_code in (p.classes or []):
				name = p.user.get_full_name() or p.user.email.split('@')[0]
				if search_query and search_query.lower() not in name.lower() and search_query.lower() not in p.degree.lower():
					continue
				shared = sorted(set(user_classes) & set(p.classes or []))
				peers.append({
					'name': name,
					'initials': _initials_for_name(name),
					'degree': p.degree or 'UQ Student',
					'year_display': p.get_year_display(),
					'gradient': _AVATAR_GRADIENTS[p.user.id % len(_AVATAR_GRADIENTS)],
					'shared_classes': shared,
					'selected_class': selected_code,
				})

	if sort_by == 'name':
		peers.sort(key=lambda p: p['name'])

	current_user_name = request.user.get_full_name() or request.user.email.split('@')[0]
	context = {
		'user_classes': user_classes,
		'selected_code': selected_code,
		'peers': peers,
		'search_query': search_query,
		'sort_by': sort_by,
		'today_label': _format_date_label(timezone.localdate()),
		'current_user_name': current_user_name,
		'current_user_initials': _initials_for_name(current_user_name),
	}
	return render(request, 'main/classmates.html', context)




@login_required
@require_http_methods(["GET"])
def get_discover_match(request):
	"""Get the next discover match for the current user"""
	try:
		# Get current user's profile
		try:
			current_profile = request.user.profile
		except StudentProfile.DoesNotExist:
			return JsonResponse({'success': False, 'message': 'Complete your profile first'}, status=400)

		# Get users the current user has already seen (liked, passed, or superlked)
		already_seen = DiscoverAction.objects.filter(user=request.user).values_list('target_user_id', flat=True)

		# Get all profiles excluding current user and already seen
		all_profiles = StudentProfile.objects.exclude(
			user_id__in=already_seen
		).exclude(
			user=request.user
		)

		# Find users who share at least one class with current user (Python-based for SQLite compatibility)
		matching_profile = None
		current_classes = set(current_profile.classes)
		
		for profile in all_profiles:
			profile_classes = set(profile.classes)
			if current_classes & profile_classes:  # Check for overlap
				matching_profile = profile
				break
		
		# If no one shares classes, just show someone else
		if not matching_profile:
			matching_profile = all_profiles.first()

		if not matching_profile:
			return JsonResponse({
				'success': True,
				'message': 'No more matches',
				'data': None
			})

		match_user = matching_profile.user

		# Find shared connection (first shared class)
		shared_classes = current_classes & set(matching_profile.classes)
		shared_connection = shared_classes.pop() if shared_classes else None

		data = {
			'id': match_user.id,
			'name': match_user.get_full_name(),
			'age': 21,  # Could be calculated from DOB if available
			'degree': matching_profile.degree,
			'year': matching_profile.get_year_display(),
			'interests': matching_profile.interests,
			'bio': matching_profile.bio,
			'shared_connection': shared_connection,
		}

		return JsonResponse({
			'success': True,
			'data': data
		})

	except Exception as e:
		return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
@require_POST
def submit_discover_action(request):
	"""Record a user's action (like, pass, or superlike) on discover"""
	try:
		data = json.loads(request.body)
		target_user_id = data.get('target_user_id')
		action_type = data.get('action_type')  # 'like', 'pass', 'superlike'

		# Validate action type
		if action_type not in dict(DiscoverAction.ActionType.choices):
			return JsonResponse({'success': False, 'message': 'Invalid action type'}, status=400)

		# Get target user
		target_user = get_object_or_404(PeerlyUser, id=target_user_id)

		# Prevent users from interacting with themselves
		if target_user == request.user:
			return JsonResponse({'success': False, 'message': 'Cannot interact with yourself'}, status=400)

		# Create or update the action
		action, created = DiscoverAction.objects.update_or_create(
			user=request.user,
			target_user=target_user,
			defaults={'action_type': action_type}
		)

		return JsonResponse({
			'success': True,
			'message': f'Action recorded: {action_type}',
			'action_id': action.id
		})

	except json.JSONDecodeError:
		return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
	except Exception as e:
		return JsonResponse({'success': False, 'message': str(e)}, status=500)


@login_required
def get_discover_stats(request):
	"""Get stats about discover interactions"""
	likes_count = DiscoverAction.objects.filter(user=request.user, action_type='like').count()
	passes_count = DiscoverAction.objects.filter(user=request.user, action_type='pass').count()
	superlikes_count = DiscoverAction.objects.filter(user=request.user, action_type='superlike').count()
	received_likes = DiscoverAction.objects.filter(target_user=request.user, action_type='like').count()

	return JsonResponse({
		'success': True,
		'stats': {
			'likes_sent': likes_count,
			'passes_sent': passes_count,
			'superlikes_sent': superlikes_count,
			'likes_received': received_likes,
		}
	})
