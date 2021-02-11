from lxml import objectify, etree
from django.db import models
from mlpool.models import *
import pandas as pd

import xml.etree.ElementTree as ElementTree
import pickle


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
        root = ElementTree.fromstring(xml)
        self.root = root
        self.project, self.task = self.parse_ids()
        df_cols = ['col0', 'col1', 'col2', 'col3']
        self.df_cols = df_cols
        self.df = self.xml2df(root)

    def parse_ids(self):
        root = self.root
        root_attrib = root.attrib
        project_id = root_attrib['project_id']
        task_id = root_attrib['task_id']

        project = Project.objects.get(id=project_id)
        task = Task.objects.get(id=task_id)

        return project, task

    def xml2df(self):
        root = self.root
        df_cols = self.df_cols
        rows = []

        for row in root:
            res = []

            for col in df_cols:
                if row is not None and row.find(col) is not None:
                    res.append(row.find(col).text)
                else:
                    res.append(None)
            rows.append({df_cols[i]: res[i] for i, _ in enumerate(df_cols)})

        return pd.DataFrame(rows, columns=df_cols)

    def get_project(self):
        return self.project

    def get_task(self):
        return self.task

    def get_input_data(self):
        return self.df


def ml_magic(input_data, task):
    ml_model = Model.objects.order_by('date_added')[-1]  # newest model
    model_path = ml_model.model_path  # TODO: think how to work with binary files

    with open(model_path, 'rb') as fid:
        estimator = pickle.load(fid)

    prediction = estimator.predict(input_data)

    return prediction, ml_model


# TODO: this function
def remember_request(project, task, input_data, target, ml_model):
    pass


# TODO: this function
def create_answer(target):
    pass


def gen_xml(project_id, task_id, data):
    xml = f"""
        <data project={project_id} task_id={task_id}>
    """

    for row in data:
        xml += f"""
            <row col0={row[0]} col1={row[1]} col2={row[2]} col3={row[3]}></row>
        """

    xml += """
        </data>
    """

    return xml


a = f"""
        <item gopa='1'>
            <field name="A">a</field>
            <field name="B">b</field>
            <field name="C">c</field>
            <field name="D">d</field>
        </item>
        """

root = ElementTree.XML(a)
for field in root:
    print(field.tag, field.attrib)
