from django.test import TestCase
import os


class SettingsTests(TestCase):

    def check_environment_key(self, key):
        try:
            os.environ[key]
        except:
            self.fail('Missing environment key {0}'.format(key))

    def test_settings(self):
        """
        Asserts required settings are defined
        """
        self.check_environment_key('DJANGO_SETTINGS_MODULE')
        self.check_environment_key('DJANGO_SECRET_KEY')
        self.check_environment_key('DJANGO_ALLOWED_HOSTS')
        self.check_environment_key('DJANGO_DATABASE_NAME')
        self.check_environment_key('DJANGO_MEDIA_ROOT')
        self.check_environment_key('DJANGO_AES_KEY')
