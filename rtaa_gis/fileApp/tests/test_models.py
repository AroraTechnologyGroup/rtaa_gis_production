from django.test import TestCase
from fileApp.models import Assignment, FileModel, GridCell
import os

os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures/json'))


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
        _assignment = Assignment.objects.create(**kwargs)
        _assignment.save()
        _assigns = Assignment.objects.all()
        self.assertTrue(len(_assigns), 5)

    def test_delete(self):
        _assign = Assignment.objects.get(pk="4")
        _assign.delete()
        _assigns = Assignment.objects.all()
        self.assertTrue(len(_assigns), 3)


# class TestFileModel(TestCase):
#     fixtures = ['filemodel', 'assignment', 'gridcell']
#
#     def setUp(self):
#         _files = FileModel.objects.all()
#         self.assertTrue(_files)
#         self._files = _files
#         pass
#
#     def test_this(self):
#         self.assertGreater(len(self._files), 1, "files in test_db")
#
#
# class TestGridCell(TestCase):
#     fixtures = ['filemodel', 'assignment', 'gridcell']
#
#     def setUp(self):
#         _grids = GridCell.objects.all()
#         self.assertTrue(_grids)
#         self._grids = _grids
#         pass
#
#     def test_this(self):
#         self.assertGreater(len(self._grids), 1, "grid cells in test_db")
