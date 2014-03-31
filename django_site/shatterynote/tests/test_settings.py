from core.tests.utils import SettingsTestsBase


class SettingsTests(SettingsTestsBase):
    """
    Checks application relative settings
    """
    def test_shatterynote_settings_envkey(self):
        self.check_environment_key('DJANGO_AES_KEY')

    def test_shatterynote_settings_formatted(self):
        try:
            from shatterynote import settings
        except Exception as e:
            self.fail("Could not import settings module: {0}".format(str(e)))
        
        self.assertIsInstance(settings.AES_KEY, bytes)
        self.assertTrue(len(settings.AES_KEY) in [16, 24, 32])
