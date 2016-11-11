from django.test import TestCase
from fileApp.models import Assignment, FileModel, GridCell
import os

os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures/json'))


class TestFileModel(TestCase):
    fixtures = ['filemodel', 'assignment', 'gridcell']

    def test_list(self):
        _files = FileModel.objects.all()
        self.assertTrue(_files)
        self.assertGreater(len(_files), 1)
        pass

    def test_get(self):
        _file = FileModel.objects.get(file_path="C:\\GitHub\\rtaa_gis\\rtaa_gis\\fileApp\\"
                                                         "fixtures\\data\\DemoDocument0.pdf")
        self.assertIsInstance(_file, FileModel)
        pass

    def test_get_assignments(self):
        _file = FileModel.objects.get(pk="6440")
        assigns = _file.assignment_set.all()
        self.assertEqual(len(assigns), 2)
        self.assertIsInstance(assigns[0], Assignment)

    def test_drop_assignment(self):
        _file = FileModel.objects.get(pk="6351")
        assign = _file.assignment_set.get(grid_cell="A01")
        self.assertIsInstance(assign, Assignment)
        assign.delete()
        assigns = _file.assignment_set.all()
        self.assertEqual(len(assigns), 0)
        pass


class TestGridCell(TestCase):
    fixtures = ['filemodel', 'assignment', 'gridcell']

    def test_list(self):
        _grids = GridCell.objects.all()
        self.assertTrue(_grids)
        self._grids = _grids
        pass

    def test_get(self):
        _grid = GridCell.objects.get(name="A14")
        self.assertIsInstance(_grid, GridCell)

    def test_create(self):
        grid_cell = GridCell.objects.create(name="ZZ00")
        grid_cell.save()
        _grid = GridCell.objects.get(name="ZZ00")
        self.assertIsInstance(_grid, GridCell)


class TestAssignment(TestCase):
    fixtures = ['filemodel', 'assignment', 'gridcell']

    def test_list(self):
        _assigns = Assignment.objects.all()
        self.assertTrue(_assigns)
        self.assertEqual(len(_assigns), 4)
        pass

    def test_create(self):
        kwargs = dict()
        kwargs['grid_cell'] = GridCell.objects.get(name="A14")
        kwargs['file'] = FileModel.objects.get(file_path="C:\\GitHub\\rtaa_gis\\rtaa_gis\\fileApp\\"
                                                         "fixtures\\data\\DemoDocument0.pdf")
        kwargs['base_name'] = 'DemoDocument0'
        kwargs['date_assigned'] = '2016-10-12'
        kwargs['comment'] = "Look how the test assignment gets added"
        _assignment = Assignment(**kwargs)
        _assignment.save()
        _assigns = Assignment.objects.all()
        self.assertTrue(len(_assigns), 5)
        pass

    def test_delete(self):
        _assign = Assignment.objects.get(pk="4")
        _assign.delete()
        _assigns = Assignment.objects.all()
        self.assertTrue(len(_assigns), 3)
        pass



