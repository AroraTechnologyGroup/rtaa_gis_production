from django.test import TestCase
from fileApp.models import Assignment, FileModel, GridCell
import os

os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures/json'))


class TestAssignment(TestCase):
    fixtures = ['filemodel', 'assignment', 'gridcell']

    def setUp(self):
        _assigns = Assignment.objects.all()
        self.assertTrue(_assigns)
        self._assigns = _assigns
        pass

    def test_build(self):
        self.assertTrue(1, "test")
        self.assertGreater(len(self._assigns), 1, "success test_build")
        pass


class TestFileModel(TestCase):
    fixtures = ['filemodel', 'assignment', 'gridcell']

    def setUp(self):
        _files = FileModel.objects.all()
        self.assertTrue(_files)
        self._files = _files
        pass

    def test_this(self):
        self.assertGreater(len(self._files), 1, "files in test_db")


class TestGridCell(TestCase):
    fixtures = ['filemodel', 'assignment', 'gridcell']

    def setUp(self):
        _grids = GridCell.objects.all()
        self.assertTrue(_grids)
        self._grids = _grids
        pass

    def test_this(self):
        self.assertGreater(len(self._grids), 1, "grid cells in test_db")
