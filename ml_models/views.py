from django.shortcuts import render
from .utils import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


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

            xml_answer = 'нихуя'

            # try:
            xml_answer = remember_and_form_result(user_request, xml, target, ml_model, project.id, task.id)
            # except:
            #     UserRequest.objects.filter(pk=user_request.pk).update(status='ERROR')
            #     user_request.refresh_from_db()

            return HttpResponse(xml_answer)

        response_id = remember_response(result, xml)  # option == response
        return HttpResponse(f'понял принял держи в курсе. id вашего запроса: {response_id}')
