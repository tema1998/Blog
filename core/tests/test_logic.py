from django.test import TestCase
from core.logic import operations
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'topblog.settings'
django.setup()

class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(6, 13, '+')
        self.assertEqual(19, result)

    def test_minus(self):
        result = operations(6, 13, '-')
        self.assertEqual(-7, result)

    def test_multiply(self):
        result = operations(6, 13, '*')
        self.assertEqual(78, result)
