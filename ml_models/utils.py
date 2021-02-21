from lxml import objectify, etree
from django.db import models
from mlpool.models import *
from .my_exceptions import *
from django.core.exceptions import *

import pandas as pd
import xml.etree.ElementTree as ElementTree
import pickle
import time as t
import datetime


class XMLParser:
    def __init__(self, xml):
        self.xml = xml
        self.root = ElementTree.XML(xml)  # TODO: допилить валидацию по xsd
        self.project, self.task, self.result = self.parse_ids()
        self.df_cols = self.get_data_columns()
        self.df = self.xml2df()

    def get_data_columns(self):
        root = self.root
        row = root.find('row')
        cols = row.attrib.keys()

        if 'id' not in cols:
            raise ColumnsError('Теги row не содержат обязательного атрибута id!')

        return list(cols)

    def parse_ids(self):
        root = self.root
        root_attrib = root.attrib
        project_id = root_attrib['project_id']
        task_id = root_attrib['task_id']

        if Project.objects.filter(id=project_id).exists():
            project = Project.objects.get(id=project_id)
        else:
            raise ObjectDoesNotExist(f'Проекта с project_id={project_id} не существует!')

        if Task.objects.filter(id=task_id, project_id=project.id).exists():
            task = Task.objects.get(id=task_id, project_id=project.id)
        else:
            raise ObjectDoesNotExist(f'В проекте с project_id={project_id} нет задачи с task_id={task_id}!')

        if 'result_id' in root_attrib:
            result_id = root_attrib['result_id']

            if Result.objects.filter(id=result_id).exists():
                result = Result.objects.get(id=result_id)
            else:
                raise ObjectDoesNotExist(f'В базе данных нет предсказаний с result_id={result_id}!')

        else:
            result = None

        return project, task, result

    def xml2df(self):
        root = self.root
        df_cols = self.df_cols
        rows = []

        for row in root.iter('row'):
            res = []
            attrib = row.attrib

            for col in df_cols:

                if row is not None and col in row.attrib.keys():
                    res.append(attrib[col])
                else:
                    res.append(None)
            rows.append({df_cols[i]: res[i] for i, _ in enumerate(df_cols)})

        return pd.DataFrame(rows, columns=df_cols).set_index('id')

    def get_project(self):
        return self.project

    def get_task(self):
        return self.task

    def get_result(self):
        return self.result

    def get_input_data(self):
        return self.df


def ml_magic(input_data, task):
    """
    Делает предсказания для входных данных.
    :param input_data: входные данные в формате pandas.DataFrame
    :param task: экземпляр класса mlpool.models.Task
    :return:
        предсказания в формате pandas.DataFrame,
        экземпляр класса mlpool.models.MLModel,
        время работы модели в миллисекундах
    """
    tick = t.time()

    if MLModel.objects.filter(task=task).exists():
        ml_model = MLModel.objects.filter(task=task).order_by('date_added')[0]  # newest model
    else:
        raise ObjectDoesNotExist(f"""Для задачи с task_id={task.id} проекта с project_id={task.project_id} пока нет ни одной модели :(""")

    model_path = str(ml_model.binary_body)

    # есть идея при ошибке чтения файла какой-то модели передавать входные данные модели которую удается прочесть,
    # но хз в таком случае придется записывать в логи что такую-то модель не удалось прочесть
    with open(model_path, 'rb') as fid:
        estimator = pickle.load(fid)

    prediction = estimator.predict(input_data)

    tack = t.time()

    return prediction, ml_model, round((tack-tick)*1e3)


def remember_request(task, ml_model, spent_time):
    """
    Записывает данные запроса в БД.
    :param task: экземпляр класса mlpool.models.Task
    :param ml_model: экземпляр класса mlpool.models.MLModel
    :param spent_time: Время затраченное на работу модели
    :return: экземпляр класса mlpool.models.UserRequest
    """
    request_data = {
        'task': task,
        'ml_model': ml_model,
        'spent_time': spent_time,
    }
    new_req = UserRequest(**request_data)
    new_req.save()

    return new_req


def remember_and_form_result(user_request, input_data, target, ml_model, project_id, task_id):
    """
    Создает запись в модели Result и пихает туда предсказанные значения для пользователя.
    :param user_request: экземпляр класса mlpool.models.UserRequest
    :param input_data: входные данные в формате xml строки
    :param target: предсказания в формате pandas.DataFrame
    :param ml_model: экземпляр класса mlpool.models.MLModel
    :param project_id: id проекта
    :param task_id: id задачи
    :return: переформатированные предсказания target в виде xml строки
    """
    result_data = {
        'ml_model': ml_model,
        'input_data': input_data,
        'user_request': user_request
    }

    new_result = Result(**result_data)
    new_result.save()

    prediction = create_answer(project_id, task_id, new_result.id, target)

    Result.objects.filter(pk=new_result.pk).update(prediction=prediction)
    new_result.refresh_from_db()

    return prediction


def create_answer(project_id, task_id, result_id, target):
    """
    Формирует ответ для пользователя в формате xml.
    :param project_id: id проекта
    :param task_id: id задачи
    :param result_id: id записи в модели Result
    :param target: предсказания в формате pandas.DataFrame
    :return: xml в виде строки
    """

    xml = f"""
        <data project_id='{project_id}' task_id='{task_id}' result_id='{result_id}'>
    """

    for index, row in target.iterrows():
        xml += f"<row id='{index}' "
        for col in row.index:
            xml += f"{col}='{row[col]}' "
        xml += '></row>\n'

    xml += """
        </data>
    """

    return xml


def remember_response(result, xml):
    """
    Записывает экспертные ответы в БД.
    :param result: экземпляр класса mlpool.models.Result
    :param xml: экспертные ответы в формате xml в виде строки
    :return: id записи в модели Response
    """
    response_attrib = {
        'result': result,
        'expert_target': xml
    }
    new_response = Response(**response_attrib)
    new_response.save()

    return new_response.id


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})

