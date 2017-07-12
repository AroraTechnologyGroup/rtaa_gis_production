from django.test import TestCase
from fileApp.models import EngineeringAssignment, EngineeringFileModel, GridCell
import os
from rtaa_gis.settings import BASE_DIR

os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures/json'))


class TestFileModel(TestCase):
    fixtures = ['engineeringfilemodel', 'engineeringassignment', 'gridcell']

    def test_list(self):
        _files = EngineeringFileModel.objects.all()
        self.assertTrue(_files)
        pass

    def test_get(self):
        t_path = os.path.join(BASE_DIR, "fileApp/fixtures/data/DemoDocument0.pdf")
        t_path = t_path.replace("\\", "/")
        _file = EngineeringFileModel.objects.filter(file_path=t_path)
        self.assertIsInstance(_file[0], EngineeringFileModel)
        pass

    def test_get_assignments(self):
        _file = EngineeringFileModel.objects.get(pk=13)
        assigns = _file.engineeringassignment_set.all()
        self.assertTrue(len(assigns))
        self.assertIsInstance(assigns[0], EngineeringAssignment)

    def test_drop_assignment(self):
        _file = EngineeringFileModel.objects.get(pk=13)
        assigns = _file.engineeringassignment_set.filter(grid_cell="A37")
        self.assertIsInstance(assigns[0], EngineeringAssignment)
        for x in assigns:
            x.delete()
        assigns = _file.engineeringassignment_set.all()
        self.assertFalse(len(assigns))
        pass


class TestGridCell(TestCase):
    fixtures = ['gridcell']

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
    fixtures = ['engineeringfilemodel', 'engineeringassignment', 'gridcell']

    def test_list(self):
        _assigns = EngineeringAssignment.objects.all()
        self.assertTrue(len(_assigns))
        self.assertIsInstance(_assigns[0], EngineeringAssignment)
        pass

    def test_create(self):
        test_file = EngineeringFileModel.objects.get(pk=5)
        grid_cell = GridCell.objects.get(name="B15")
        kwargs = {
            'grid_cell': grid_cell,
            'file': test_file,
            'comment': "Look how the test assignment gets added"
        }

        _assignment = EngineeringAssignment(**kwargs)
        _assignment.save()

        _assigns = EngineeringAssignment.objects.all()
        self.assertTrue(len(_assigns))
        new_obj = EngineeringAssignment.objects.filter(file=5).filter(grid_cell=grid_cell)
        self.assertIsInstance(new_obj[0], EngineeringAssignment)
        pass

    def test_delete(self):
        _assign = EngineeringAssignment.objects.get(pk="4")
        _assign.delete()
        _assigns = EngineeringAssignment.objects.filter(pk='4')
        self.assertFalse(len(_assigns))
        pass



