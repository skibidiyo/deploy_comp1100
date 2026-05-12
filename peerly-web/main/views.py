from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

def landing_page(request):
	return render(request, 'main/landing.html')

def _redirect_if_onboarding_not_needed(request):
	if not request.user.is_authenticated:
		return redirect('login')
	if not request.session.get('needs_onboarding'):
		return redirect('dashboard')
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
	return redirect('dashboard')
