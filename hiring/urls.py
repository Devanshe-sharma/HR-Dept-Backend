# hiring/urls.py
from django.urls import path
from . import views
from django.http import JsonResponse


def api_root(request):
    return JsonResponse({
        "next_serial": "/api/next-serial/",
        "departments": "/api/departments/",
        "employees": "/api/employees/",
        "designations": "/api/designations/",
        "submit": "/api/submit/"
    })

urlpatterns = [
    path('', api_root),  # handles /api/
    path('next-serial/', views.next_serial),
    path('departments/', views.get_departments),
    path('employees/', views.employees),
    path('designations/', views.all_designations),
    path('submit/', views.submit_requisition),
]