# hiring/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('next-serial/', views.next_serial),
    path('departments/', views.get_departments),
    path('employees/', views.get_employees),
    path('designations/', views.all_designations),
    path('submit/', views.submit_requisition),
      # ← MAKE SURE THIS MATCHES
]