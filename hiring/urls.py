from django.urls import path
from . import views

urlpatterns = [
    # --- Core HR data ---
    path('departments/', views.get_departments, name='departments'),
    path('designations/', views.all_designations, name='designations'),
    path('employees/', views.employees, name='employees'),

    # --- Hiring Requisition ---
    path('next-serial/', views.next_serial, name='next-serial'),
    path('requisitions/', views.all_requisitions, name='all-requisitions'),
    path('requisition/<int:pk>/', views.requisition_detail, name='requisition-detail'),
    path('submit-requisition/', views.submit_requisition, name='submit-requisition'),

    # --- Candidate Applications ---
    path('candidate-applications/', views.all_candidate_applications, name='all-candidate-applications'),
    path('candidate-application/<int:pk>/', views.candidate_application_detail, name='candidate-application-detail'),
    path('submit-candidate/', views.submit_candidate_application, name='submit-candidate'),

    # --- Onboarding ---
    path('onboardings/', views.all_onboardings, name='all-onboardings'),
    path('onboarding/<int:pk>/', views.onboarding_detail, name='onboarding-detail'),
    path('submit-onboarding/', views.submit_onboarding, name='submit-onboarding'),

    # --- Onboarding Updates ---
    path('onboarding-updates/', views.all_onboarding_updates, name='all-onboarding-updates'),
    path('onboarding-update/<int:pk>/', views.onboarding_update_detail, name='onboarding-update-detail'),
    path('submit-onboarding-update/', views.submit_onboarding_update, name='submit-onboarding-update'),
]
