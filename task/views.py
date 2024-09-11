from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to a page showing the list of tasks
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'task/edit_task.html', {'form': form, 'task': task})


@csrf_exempt
def update_task_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            new_status = data.get('status')

            # Find the task and update its status
            task = Task.objects.get(id=task_id)
            task.status = new_status
            task.save()

            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to a task list or another view after saving
    else:
        form = TaskForm()
    
    return render(request, 'task/create_task.html', {'form': form})

def task_view(request):
    tasks = Task.objects.all()
    return render(request, 'task/index.html', {'tasks': tasks})


@csrf_exempt
def restore_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')

            task = Task.objects.get(id=task_id)
            task.status = 'pending'  # Restore task to pending status
            task.save()

            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def delete_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')

            task = Task.objects.get(id=task_id)
            task.delete()

            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})