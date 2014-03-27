from core.tests.utils import SettingsTestsBase


class SettingsTests(SettingsTestsBase):

    def test_share_setting_share(self):
        self.check_environment_key('DJANGO_AES_KEY')
