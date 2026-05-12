from django.shortcuts import render

def landing_page(request):
	return render(request, 'main/landing.html')

def onboarding_step1(request):
	return render(request, 'main/onboarding.html')

def onboarding_step2(request):
	return render(request, 'main/onboarding_step2.html')

def onboarding_step3(request):
	return render(request, 'main/onboarding_step3.html')

def onboarding_step4(request):
	return render(request, 'main/onboarding_step4.html')

def onboarding_step5(request):
	return render(request, 'main/onboarding_step5.html')
