from django.shortcuts import render
from .utils import *
from django.http import HttpResponse
from .utils import gen_xml
from django.views.decorators.csrf import csrf_exempt
import time


@csrf_exempt
def index(request):
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

            return HttpResponse(xml_answer)

        remember_response(result, xml)  # option == response
        return HttpResponse('понял принял держи в курсе')





