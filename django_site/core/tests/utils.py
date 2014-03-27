from django.test import TestCase
import os


class SettingsTestsBase(TestCase):
    
    def check_environment_key(self, key):
        try:
            value = os.environ[key]
        except:
            self.fail('Missing environment key {0}'.format(key))
        self.assertIsNotNone(value)
        self.assertNotEqual(value, '')
