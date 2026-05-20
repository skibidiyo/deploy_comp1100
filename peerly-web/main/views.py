from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

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
	request.session.pop('needs_onboarding', None)
	return redirect('home')

@login_required
def dashboard(request):
	"""Home/Discover page shown after login or onboarding completion"""
	return render(request, 'main/dashboard.html')

@login_required
def campus_events(request):
	return render(request, 'main/campus_events.html')
