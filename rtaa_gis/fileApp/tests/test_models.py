from django.test import TestCase
from fileApp.models import Assignment, FileModel, GridCell
from fileApp.serializers import FileSerializer, GridSerializer

import os
fixture_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'fixtures/json')
os.chdir(fixture_folder)
file_serializer = FileSerializer('filemodel.json')
file_serializer.data
# assignments = open('assignment.json', 'rb')


# class TestAssignment(TestCase):
#     fixtures = ['assignment.json']
#
#     def setUp(self):
#         assign = Assignment.objects.get({"pk": 1})
#         self.assertTrue(assign)
#         pass
#
#     def test_1(self):
#         self.assertTrue(1, "test")
#         pass
#

class TestFileModel(TestCase):
    fixtures = ['filemodel.json']

    def test_this(self):
        objs = FileModel.objects.all()

        self.assertGreater(len(objs), 1, "four is good")


class TestGridCell(TestCase):
    fixtures = ['gridcell.json']

    def test_this(self):
        objs = GridCell.objects.all()
        self.assertGreater(len(objs), 1, "four is good")
