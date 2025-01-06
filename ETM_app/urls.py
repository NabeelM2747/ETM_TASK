"""
URL configuration for ETM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    # Employee CRUD URLs
    path('users/', views.get_users, name='get_users'),  # List all users
    path('users/<int:user_id>/', views.get_user, name='get_user'),  # Get a single user by ID
    path('users/create/', views.create_user, name='create_user'),  # Create a new user
    path('users/update/', views.update_user, name='update_user'),  # Update a user
    path('users/delete/', views.delete_user, name='delete_user'),  # Delete a user
    # Task CRUD URLs
    path('tasks/create/', views.create_task, name='create_task'),  # create a new task
    path('tasks/', views.get_all_tasks, name='get_all_tasks'),  # Fetch all tasks
    path('tasks/employee_tasks/', views.get_tasks_by_employee, name='get_tasks_by_employee'), # Fetch task of one employee
    path('tasks/admin-manage-tasks/', views.admin_manage_tasks, name='admin_manage_tasks'), # Create comment on a task
    # Weekly Excel Report Generation URL
    path('tasks/export/', views.export_tasks_to_excel, name='export_tasks_to_excel'),
]
