from django.test import TestCase
from .views import *
from .utils import *

import pandas as pd


# class XMLParserTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         xml_cases = [
#             """
#             <data project_id='1' task_id='1' operation='request'>
#                     <row id='1' col0='1' col1='2' col2='3' col3='4' ></row>
#                     <row id='2' col0='5' col1='6' col2='7' col3='8' ></row>
#                     <row id='3' col0='1' col1='2' col2='3' col3='4' ></row>
#                     <row id='4' col0='4' col1='3' col2='2' col3='1' ></row>
#             </data>
#             """,
#             """
#             <data project_id='1' task_id='2' operation='response' result_id='1'>
#                     <row id='1' y='1' ></row>
#                     <row id='2' y='5' ></row>
#                     <row id='3' y='1' ></row>
#                     <row id='4' y='4' ></row>
#             </data>
#             """,
#             """
#             <data project_id='1' task_id='1' operation='request'>
#                     <row id='1' col0='1' col1='2' col2='3' col3='4' ></row>
#                     <row id='2' col0='5' col1='6' col2='7' col3='8' ></row>
#                     <row id='3' col0='1' col1='2' col2='3' col3='4' ></row>
#                     <row id='4' col0='4' col1='3' col2='2' col3='1' ></row>
#             </data>
#             """
#         ]
#
#         correct_xml_indexes = [0, 1]
#         incorrect_xml_indexes = [x for x in range(len(xml_cases)) if x not in correct_xml_indexes]
#
#         cls.xml_cases = xml_cases
#         cls.correct_xml_indexes = correct_xml_indexes
#         cls.incorrect_xml_indexes = incorrect_xml_indexes


class UtilsTestCase(TestCase):
    def test_create_answer(self):
        targets = (
            [[1, 'cat'],
             [2, 'dog']],
            [['1', 'cat'],
             ['2', 'dog']],
            [['1', 'cat', 'aboba'],
             ['2', 'dog', 'obama']],
            [['1', 'cat', 'aboba'],
             ['1', 'dog', 'obama']],
            [[1, 123, 0.03],
             [2, 345.01, 141.12]],

        )
        columns = (
            ['id', 'y'],
            ['id', 'y'],
            ['id', 'y', 'y2'],
            ['id', 'y', 'y2'],
            ['id', 'y', 'y2'],
            ['id', 'y', 'y2'],
        )

        proper_targets = (
            """
            <data project_id='1' task_id='1' result_id='1'>
                <row id='1' y='cat'></row>
                <row id='2' y='dog'></row>
            </data>
            """,
            """
            <data project_id='1' task_id='1' result_id='1'>
                <row id='1' y='cat'></row>
                <row id='2' y='dog'></row>
            </data>
            """,
            """
            <data project_id='1' task_id='1' result_id='1'>
                <row id='1' y='cat' y2='aboba'></row>
                <row id='2' y='dog' y2='obama'></row>
            </data>
            """,
            """
            <data project_id='1' task_id='1' result_id='1'>
                <row id='1' y='cat' y2='aboba'></row>
                <row id='1' y='dog' y2='obama'></row>
            </data>
            """,
            """
            <data project_id='1' task_id='1' result_id='1'>
                <row id='1' y='123.0' y2='0.03'></row>
                <row id='2' y='345.01' y2='141.12'></row>
            </data>
            """,
            """
            <data project_id='1' task_id='1' result_id='1'>
                <row id='1' y='123' y2='0'></row>
                <row id='2' y='345' y2='141'></row>
            </data>
            """,
        )

        for t, p, cols in zip(targets, proper_targets, columns):
            df = pd.DataFrame(t, columns=cols).set_index('id')
            answer = create_answer(1, 1, 1, df)

            self.assertXMLEqual(answer, p)
