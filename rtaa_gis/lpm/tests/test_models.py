from django.test import TestCase
from lpm.models import Agreement, Space
import os

# setting this environment variable allows fixtures to be loaded
os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures/json'))


class TestAgreement(TestCase):
    fixtures = ['agreement', 'space']

    def test_list(self):
        _files = Agreement.objects.all()
        self.assertTrue(_files)
        pass

    def test_get(self):
        id = 1129
        _agreement = Agreement.objects.filter(id=id)
        self.assertIsInstance(_agreement[0], Agreement)
        pass

    def test_get_spaces(self):
        _agreement = Agreement.objects.get(id=1129)
        assigned_spaces = _agreement.space_set.all()
        self.assertTrue(len(assigned_spaces))
        self.assertIsInstance(assigned_spaces[0], Space)

    # def test_link_space(self):
    #     _agreement = Agreement.objects.get(id=1129)
    #
    # def test_drop_assignment(self):
    #     _agreement = Agreement.objects.get(id=1129)
    #     assigns = _agreement.space_set.filter(="A04")
    #     self.assertIsInstance(assigns[0], EngineeringAssignment)
    #     for x in assigns:
    #         x.delete()
    #     assigns = _file.engineeringassignment_set.all()
    #     self.assertFalse(len(assigns))
    #     pass


class TestSpace(TestCase):
    fixtures = ['agreement', 'space']

    def test_list(self):
        _spaces = Space.objects.all()
        self.assertTrue(_spaces)
        self._spaces = _spaces
        pass

    def test_get(self):
        _space = Space.objects.get(id="A14")
        self.assertIsInstance(_space, Space)

    def test_create(self):
        space = Space.objects.create(id="ZZ00")
        space.save()
        _space = Space.objects.get(id="ZZ00")
        self.assertIsInstance(_space, Space)
