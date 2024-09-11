from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_view, name='task_list'),
    path('create/', views.create_task, name='create_task'),  # Ensure this is correct
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path('restore-task/', views.restore_task, name='restore_task'),
    path('delete-task/', views.delete_task, name='delete_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),  # This should match the view name
]