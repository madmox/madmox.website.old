from django.test import TestCase


class SettingsTests(TestCase):
    """
    Checks application relative settings
    """
    def test_settings(self):
        try:
            from shatterynote import settings
        except Exception as e:
            self.fail("Could not import settings module: {0}".format(str(e)))
        
        self.assertIsInstance(settings.AES_KEY, bytes)
        self.assertTrue(len(settings.AES_KEY) in [16, 24, 32])
