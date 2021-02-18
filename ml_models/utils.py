from lxml import objectify, etree
from django.db import models
from mlpool.models import *
import pandas as pd

import xml.etree.ElementTree as ElementTree
import pickle
import time as t
import datetime


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


class XMLParser:
    def __init__(self, xml):
        self.xml = xml
        self.root = ElementTree.XML(xml)
        self.project, self.task, self.result = self.parse_ids()
        self.df_cols = self.get_data_columns()
        self.df = self.xml2df()

    def get_data_columns(self):
        root = self.root
        row = root.find('row')
        cols = row.attrib.keys()

        return list(cols)

    def parse_ids(self):
        root = self.root
        root_attrib = root.attrib
        project_id = root_attrib['project_id']
        task_id = root_attrib['task_id']

        project = Project.objects.get(id=project_id)
        task = Task.objects.get(id=task_id)

        if 'result_id' in root_attrib:
            result_id = root_attrib['result_id']
            result = Result.objects.get(id=result_id)
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

        return pd.DataFrame(rows, columns=df_cols)

    def get_project(self):
        return self.project

    def get_task(self):
        return self.task

    def get_result(self):
        return self.result

    def get_input_data(self):
        return self.df


def ml_magic(input_data, task):
    tick = t.time()
    ml_model = MLModel.objects.filter(task=task).order_by('date_added')[0]  # newest model
    model_path = str(ml_model.binary_body)

    with open(model_path, 'rb') as fid:
        estimator = pickle.load(fid)

    prediction = estimator.predict(input_data)

    return prediction, ml_model, datetime.time(microsecond=round((t.time() - tick)*1000))


def remember_request(task, ml_model, spent_time):
    request_data = {
        'task': task,
        'ml_model': ml_model,
        'spent_time': spent_time,
    }
    new_req = UserRequest(**request_data)
    new_req.save()

    return new_req


def remember_result(user_request, input_data, ml_model):
    result_data = {
        'ml_model': ml_model,
        'input_data': input_data,
        'user_request': user_request,
    }
    new_result = Result(**result_data)
    new_result.save()

    return new_result


def create_answer(project_id, task_id, result, target):
    xml = f"""
        <data project_id='{project_id}' task_id='{task_id}' result_id='{result.id}'>
    """

    for elem in target:
        xml += f"""
            <row y='{elem}'></row>
        """

    xml += """
        </data>
    """

    Result.objects.filter(pk=result.pk).update(prediction=target)
    result.refresh_from_db()

    return xml


def gen_xml(project_id, task_id, data, data_columns, operation="request"):
    xml = f"""
        <data project_id='{project_id}' task_id='{task_id}' operation='{operation}'>
    """

    for row in data:
        xml += "<row "

        for i, col in enumerate(data_columns):
            xml += f"""{col}='{row[i]}' """

        xml += "></row>"

    xml += """
        </data>
    """

    return xml


def remember_response(result, xml):
    response_attrib = {
        'result': result,
        'result_id': result.id,
        'expert_target': xml
    }
    new_response = Response(**response_attrib)
    new_response.save()

    return new_response.id


# <data project_id='1' task_id='1' operation='request'>
#     <row col0='1' col1='2' col2='3'></row>
#     <row col0='1' col1='2' col2='3'></row>
# </data>
