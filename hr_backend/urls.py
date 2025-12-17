from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect   # <-- add this

def root_redirect(request):
    return redirect('/')   # or redirect('/api/') or to your React index.html

urlpatterns = [
    path('', root_redirect),
    path('admin/', admin.site.urls),
    path('api/', include('hiring.urls')),
]