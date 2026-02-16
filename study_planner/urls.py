from django.contrib import admin
from django.urls import path, include
from core.views import dashboard, toggle_task, register, delete_task 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('toggle-task/<int:task_id>/', toggle_task, name='toggle_task'),
    path('delete-task/<int:task_id>/', delete_task, name='delete_task'), # views. silindi
    path('accounts/', include('django.contrib.auth.urls')),
]