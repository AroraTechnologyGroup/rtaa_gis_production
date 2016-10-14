#!/usr/bin/env python
import django
from django.conf import settings
from django.test.utils import get_runner
import unittest
import os, sys

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["fileApp.tests"])
    sys.exit(bool(failures))
