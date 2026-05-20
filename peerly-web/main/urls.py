from django.urls import path

from .views import campus_events, complete_onboarding, dashboard, landing_page, onboarding_step1, onboarding_step2, onboarding_step3, onboarding_step4, onboarding_step5

urlpatterns = [
    path('', landing_page, name='landing-page'),
    path('home/', dashboard, name='home'),
    path('events/', campus_events, name='campus-events'),
    path('onboarding/step1/', onboarding_step1, name='onboarding-step1'),
    path('onboarding/step2/', onboarding_step2, name='onboarding-step2'),
    path('onboarding/step3/', onboarding_step3, name='onboarding-step3'),
    path('onboarding/step4/', onboarding_step4, name='onboarding-step4'),
    path('onboarding/step5/', onboarding_step5, name='onboarding-step5'),
    path('onboarding/complete/', complete_onboarding, name='complete-onboarding'),
]
