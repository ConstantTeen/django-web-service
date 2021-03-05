from django.shortcuts import render


def index(request):
    return render(request, 'easy_using/index.html')


def new_request(request):
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
    return render(request, 'easy_using/new_request.html', context)


def new_response(request):
    return render(request, 'easy_using/new_response.html')
