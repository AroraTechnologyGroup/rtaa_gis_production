from django.test import TestCase
import logging
import sys
import os
from rtaa_gis import settings
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rtaa_gis.settings'
django.setup()

# Create your tests here.
logger = logging.getLogger('_fileApp')
logger.error("This is a test error")

