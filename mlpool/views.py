from django.shortcuts import render, redirect
from .models import *
from .forms import *


def index(request):
    return render(request, 'mlpool/index.html')


def projects(request):
    projects = Project.objects.all()
    user_in_projects = UserInProject.objects.filter(user=request.user)
    user_projects_list = [x.project for x in list(user_in_projects)]
    other_projects = [x for x in projects if x not in user_projects_list]

    context = {
        'projects': projects,
        'user_projects': user_projects_list,
        'other_projects': other_projects
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
    task_models = Model.objects.filter(task_id=task_id)
    task_project = task.project
    requests = Request.objects.filter(user=request.user)

    context = {
        'task': task,
        'models': task_models,
        'project': task_project,
        'requests': requests
    }
    return render(request, 'mlpool/task.html', context)

