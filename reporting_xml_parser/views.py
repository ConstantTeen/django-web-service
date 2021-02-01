from django.shortcuts import render, redirect
from ..mlpool.models import Project
from .forms import *
from .utils import ml_magic

def index(request):
    projects = Project.objects.all()

    context = {
        'projects': projects
    }
    return render(request, 'xml/index.html', context)


def new_request(request, project_id):
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = RequestForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = RequestForm(data=request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.user = request.user
            new_request.save()
            # TODO: make a prediction with ml model, create a Model with answers of ml model
            ml_magic(new_request)
            # TODO: сделать редирект на реквест
            return redirect('xml:user_request', new_request.id)
    # Вывести пустую или недействительную форму.
    context = {
        'form': form,
        'project': Project.objects.get(id=project_id)
    }

    return render(request, 'xml/new_request.html', context)


def user_request(request, request_id):
    req = Request.objects.get(id=request_id)

    context = {
        'request': req,
    }
    return render(request, 'xml/request_info.html')