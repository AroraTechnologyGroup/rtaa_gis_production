import django
from django.conf import settings
import unittest
import os, sys
from unittest import TestResult
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rtaa_gis.settings'
BASE_DIR = settings.BASE_DIR

import fileApp
from fileApp.tests import test_models, test_views, test_serializers

if __name__ == '__main__':
    res = TestResult()
    loader = unittest.TestLoader()
    x = loader.discover(start_dir=os.path.join(BASE_DIR, 'fileApp/tests/'))
    x.run(res)
