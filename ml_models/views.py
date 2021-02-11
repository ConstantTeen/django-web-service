from django.shortcuts import render
from .utils import *
from django.http import HttpResponse
from .utils import gen_xml


# TODO: test this
def index(request):
    if request.method == 'GET':
        context = {'xml': gen_xml(1, 1, [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [1, 2, 3, 4],
            [4, 3, 2, 1],
        ])}
        return render(request, 'ml_models/index.html', context)

    if request.method == 'POST':
        xml = request.POST['xml']
        xml.emc
        print(xml)
        parser = XMLParser(xml)

        project = parser.get_project()
        task = parser.get_task()
        input_data = parser.get_input_data()

        # target, ml_model = ml_magic(input_data, task)
        #
        # remember_request(project, task, input_data, target, ml_model)
        #
        # answer = create_answer(target)
        #
        # return answer

        print(project, task, input_data)

        return HttpResponse(xml)



