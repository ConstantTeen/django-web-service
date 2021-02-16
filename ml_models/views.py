from django.shortcuts import render
from .utils import *
from django.http import HttpResponse
from .utils import gen_xml
import time


def index(request):
    if request.method == 'GET':
        context = {'xml': gen_xml(1, 1, [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [1, 2, 3, 4],
            [4, 3, 2, 1],
        ], data_columns=['col0', 'col1', 'col2', 'col3'])}
        return render(request, 'ml_models/index.html', context)

    if request.method == 'POST':
        xml = request.POST['xml']
        option = request.POST['option']

        parser = XMLParser(xml)

        project = parser.get_project()
        task = parser.get_task()
        result = parser.get_result()
        input_data = parser.get_input_data()

        if option == 'request':
            target, ml_model, spent_time = ml_magic(input_data, task)

            user_request = remember_request(task, ml_model, spent_time)

            result = remember_result(user_request, xml, ml_model)

            xml_answer = create_answer(project.id, task.id, result, target)

            return HttpResponse('готово')

        remember_response(result, xml)  # option == response
        return HttpResponse('понял принял держи в курсе')





