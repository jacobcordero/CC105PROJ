from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import date

def task_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        status = 'Upcoming' if due_date and date.fromisoformat(due_date) > date.today() else 'Due Today'
        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            status=status
        )
        return redirect('task_list')  # Use named URL for redirection
    return render(request, 'task_create.html')

def task_list(request):
    tasks = Task.objects.all()
    today = date.today()
    for task in tasks:
        if task.due_date and task.due_date < today:
            task.status = 'Overdue'
            task.css_class = 'text-danger'  # Add CSS class for overdue
        elif task.due_date == today:
            task.status = 'Due Today'
            task.css_class = 'text-warning'  # Add CSS class for due today
        else:
            task.status = 'Upcoming'
            task.css_class = 'text-success'  # Add CSS class for upcoming
        task.save()
    return render(request, 'task_list.html', {'tasks': tasks, 'task_ids': [task.id for task in tasks]})

def task_update(request, id):  # Ensure parameter name matches the URL pattern
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.due_date = request.POST['due_date']
        task.status = 'Upcoming' if task.due_date and date.fromisoformat(task.due_date) > date.today() else 'Overdue'
        task.save()
        return redirect('task_list')  # Use named URL for redirection
    return render(request, 'task_update.html', {'task': task})

def task_delete(request, id):  # Ensure parameter name matches the URL pattern
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':  # Confirm deletion
        task.delete()
        return redirect('task_list')  # Use named URL for redirection
    return render(request, 'task_delete.html', {'task': task})  # Render confirmation page