from django.shortcuts import render, redirect
from .models import *
from .forms import *


def index(request):
    return render(request, 'mlpool/index.html')


def projects(request):
    projects = Project.objects.all()

    context = {
        'projects': projects,
    }

    return render(request, 'mlpool/projects.html', context)


def project(request, project_id):
    project = Project.objects.get(id=project_id)
    tasks = project.task_set.all()

    context = {
        'project': project,
        'tasks': tasks
    }
    return render(request, 'mlpool/project.html', context)


def task(request, task_id):
    task = Task.objects.get(id=task_id)
    task_models = MLModel.objects.filter(task=task)
    task_project = task.project

    context = {
        'task': task,
        'models': task_models,
        'project': task_project,
    }
    return render(request, 'mlpool/task.html', context)


def new_ml_model(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = MLModelForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = MLModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_model = form.save(commit=False)
            new_model.task = task
            new_model.author = request.user
            new_model.save()
            return redirect('mlpool:task', task_id=task_id)
    # Вывести пустую или недействительную форму.
    context = {'task': task, 'form': form}
    return render(request, 'mlpool/new_ml_model.html', context)
