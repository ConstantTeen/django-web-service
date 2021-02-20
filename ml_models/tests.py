from django.test import TestCase
from .views import *
from .utils import *


class XMLParserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        xml_cases = [
            """
            <data project_id='1' task_id='1' operation='request'>    
                    <row id='1' col0='1' col1='2' col2='3' col3='4' ></row>
                    <row id='2' col0='5' col1='6' col2='7' col3='8' ></row>
                    <row id='3' col0='1' col1='2' col2='3' col3='4' ></row>
                    <row id='4' col0='4' col1='3' col2='2' col3='1' ></row>       
            </data>
            """,
            """
            <data project_id='1' task_id='2' operation='response' result_id='1'>    
                    <row id='1' y='1' ></row>
                    <row id='2' y='5' ></row>
                    <row id='3' y='1' ></row>
                    <row id='4' y='4' ></row>       
            </data>
            """,
            """
            <data project_id='1' task_id='1' operation='request'>    
                    <row id='1' col0='1' col1='2' col2='3' col3='4' ></row>
                    <row id='2' col0='5' col1='6' col2='7' col3='8' ></row>
                    <row id='3' col0='1' col1='2' col2='3' col3='4' ></row>
                    <row id='4' col0='4' col1='3' col2='2' col3='1' ></row>       
            </data>
            """
        ]

        correct_xml_indexes = [0, 1]
        incorrect_xml_indexes = [x for x in range(len(xml_cases)) if x not in correct_xml_indexes]

        cls.xml_cases = xml_cases
        cls.correct_xml_indexes = correct_xml_indexes
        cls.incorrect_xml_indexes = incorrect_xml_indexes


class UtilsTestCase(TestCase):
    def test_create_answer(self):
        # project_id, task_id, result_id, target = 1,1,1,
        targets = (
            [[1, 'cat'],
             [2, 'dog'],
             [4, 'cat'],
             [6, 'cat']],
            [[1, 'cat'],
             [2, 'cat'],
             [8, 'cat']],
            [[1, 'cat'],
             [2, 'cat'],
             [4, 'cat'],
             [6, 'cat'],
             [8, 'cat']],
            [[1, 'cat'],
             [2, 'cat'],
             [4, 'cat'],
             [6, 'cat'],
             [8, 'cat']],
        )

