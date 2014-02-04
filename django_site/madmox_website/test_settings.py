from django.test import TestCase
import os


def test_environment_key(key):
    try:
        key = 'DJANGO_SETTINGS_MODULE'
        os.environ[key]
    except:
        self.fail('Missing environment key {0}'.format(key))


class SettingsTests(TestCase):
    def test_settings(self):
        """
        Asserts required settings are defined
        """
        test_environment_key('DJANGO_SETTINGS_MODULE')
        test_environment_key('DJANGO_SECRET_KEY')
        test_environment_key('DJANGO_ALLOWED_HOSTS')
        test_environment_key('DJANGO_DATABASE_NAME')
        test_environment_key('DJANGO_MEDIA_ROOT')
        test_environment_key('DJANGO_AES_KEY')
