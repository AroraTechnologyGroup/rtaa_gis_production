from django.test import TestCase
from fileApp.models import Assignment, FileModel, GridCell
import os

os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures/json'))


class TestAssignment(TestCase):
    fixtures = ['filemodel', 'assignment', 'gridcell']

    def setUp(self):
        assign = Assignment.objects.get({"pk": 1})
        self.assertTrue(assign)
        pass

    def test_1(self):
        self.assertTrue(1, "test")
        pass


class TestFileModel(TestCase):
    fixtures = ['filemodel', 'assignment', 'gridcell']

    def test_this(self):
        objs = FileModel.objects.all()

        self.assertGreater(len(objs), 1, "four is good")


class TestGridCell(TestCase):
    fixtures = ['filemodel', 'assignment', 'gridcell']

    def test_this(self):
        objs = GridCell.objects.all()
        self.assertGreater(len(objs), 1, "four is good")
