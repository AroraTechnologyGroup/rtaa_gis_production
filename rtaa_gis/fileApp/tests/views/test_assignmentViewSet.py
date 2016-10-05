from django.test import TestCase
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'


class TestAssignmentViewSet(TestCase):
    def test__clean(self):
        self.fail()
