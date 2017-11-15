from django.test import TestCase
from cloudSync.models import GDB, FeatureDataset, FeatureClass, FeatureLayer, WebMap, PublisherLog
import os

# setting this environment variable allows fixtures to be loaded
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures/json'))


class TestGDB(TestCase):
    fixtures = ['gdb']

    def test_list(self):
        _gdb = GDB.objects.all()
        self.assertTrue(_gdb)
        pass

    def test_get(self):
        t_path = "//renofs2/groups/engineering/drawings/std/06_4sd_alp.pdf"
        _file = EngineeringFileModel.objects.filter(file_path=t_path)
        self.assertIsInstance(_file[0], EngineeringFileModel)
        pass

    def test_get_assignments(self):
        _file = EngineeringFileModel.objects.get(pk=51959)
        assigns = _file.engineeringassignment_set.all()
        self.assertTrue(len(assigns))
        self.assertIsInstance(assigns[0], EngineeringAssignment)

    def test_drop_assignment(self):
        _file = EngineeringFileModel.objects.get(pk=51959)
        assigns = _file.engineeringassignment_set.filter(grid_cell="L21")
        self.assertIsInstance(assigns[0], EngineeringAssignment)
        for x in assigns:
            x.delete()
        assigns = _file.engineeringassignment_set.filter(grid_cell="L21")
        self.assertFalse(len(assigns))
        pass
