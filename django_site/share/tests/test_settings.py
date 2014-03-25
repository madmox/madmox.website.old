from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured


class TestSettings(TestCase):
    def test_share_setting_share(self):
        from share import settings
        self.assertNotEqual(settings.SHARE_ROOT, '')
