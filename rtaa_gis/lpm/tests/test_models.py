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

    def test_filter(self):
        id = 1129
        _agreement = Agreement.objects.filter(id=id)
        self.assertIsInstance(_agreement[0], Agreement)
        pass

    def test_get_spaces(self):
        _agreement = Agreement.objects.get(id=2105)
        assigned_spaces = _agreement.space_set.all()
        self.assertTrue(len(assigned_spaces))
        self.assertIsInstance(assigned_spaces[0], Space)

    def test_link_space(self):
        _agreement = Agreement.objects.get(id=1129)
        _space = Space.objects.create(id="Test")
        _agreement.space_set.add(_space)
        _agreement = Agreement.objects.get(id=1129)
        cnt = len(_agreement.space_set.all())
        self.assertEqual(cnt, 1)

    def test_drop_space(self):
        _agreement = Agreement.objects.get(id=2307)
        spaces = _agreement.space_set.filter(id="A04")
        for x in spaces:
            x.agreement = None
            x.save()
        spaces = _agreement.space_set.all()
        self.assertFalse(len(spaces))


class TestSpace(TestCase):
    fixtures = ['agreement', 'space']

    def test_list(self):
        _spaces = Space.objects.all()
        self.assertTrue(_spaces)
        pass

    def test_get(self):
        _space = Space.objects.get(id="A12")
        self.assertIsInstance(_space, Space)

    def test_create(self):
        space = Space.objects.create(id="ZZ00")
        space.save()
        _space = Space.objects.get(id="ZZ00")
        self.assertIsInstance(_space, Space)

    def test_link_agreement(self):
        agreement = Agreement.objects.get(id=1129)
        sp = Space.objects.get(id="A12")
        sp.agreement = agreement
        sp.save()
        space = Space.objects.get(id="A12")
        self.assertIsInstance(space.agreement, Agreement)
        pass

    def test_drop_agreement(self):
        space = Space.objects.get(id="A12")
        space.agreement = None
        space.save()
        space = Space.objects.get(id="A12")
        self.assertIsNone(space.agreement)
