from core.tests.utils import SettingsTestsBase


class SettingsTests(SettingsTestsBase):

    def test_settings(self):
        """
        Asserts required settings are defined
        """
        self.check_environment_key('DJANGO_SETTINGS_MODULE')
        self.check_environment_key('DJANGO_SECRET_KEY')
        self.check_environment_key('DJANGO_ALLOWED_HOSTS')
        self.check_environment_key('DJANGO_DATABASE_NAME')
        self.check_environment_key('DJANGO_MEDIA_ROOT')
