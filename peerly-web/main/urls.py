from django.urls import path

from .views import (
    campus_events, classmates_page, complete_onboarding, dashboard, groups_page, landing_page,
    onboarding_step1, onboarding_step2, onboarding_step3, onboarding_step4, onboarding_step5,
    add_class, get_discover_match, submit_discover_action, get_discover_stats,
    create_study_session, toggle_study_session,
    create_community, toggle_community,
)

urlpatterns = [
    path('', landing_page, name='landing-page'),
    path('home/', dashboard, name='home'),
    path('events/', campus_events, name='campus-events'),
    path('groups/', groups_page, name='groups'),
    path('classmates/', classmates_page, name='classmates'),
    path('add-class/', add_class, name='add-class'),
    path('discover/match/', get_discover_match, name='discover-match'),
    path('discover/action/', submit_discover_action, name='discover-action'),
    path('discover/stats/', get_discover_stats, name='discover-stats'),
    path('onboarding/step1/', onboarding_step1, name='onboarding-step1'),
    path('onboarding/step2/', onboarding_step2, name='onboarding-step2'),
    path('onboarding/step3/', onboarding_step3, name='onboarding-step3'),
    path('onboarding/step4/', onboarding_step4, name='onboarding-step4'),
    path('onboarding/step5/', onboarding_step5, name='onboarding-step5'),
    path('onboarding/complete/', complete_onboarding, name='complete-onboarding'),
    path('study-sessions/create/', create_study_session, name='create-study-session'),
    path('study-sessions/<int:session_id>/toggle/', toggle_study_session, name='toggle-study-session'),
    path('communities/create/', create_community, name='create-community'),
    path('communities/<int:community_id>/toggle/', toggle_community, name='toggle-community'),
]
