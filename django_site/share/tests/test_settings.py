from core.tests.utils import SettingsTestsBase
import os.path
import posixpath


class SettingsTests(SettingsTestsBase):

    def test_share_setting_share(self):
        try:
            from share import settings
        except Exception as e:
            self.fail("Could not import settings module: {0}".format(str(e)))
        
        # Assert path is absolute and exists
        self.assertTrue(os.path.isabs(settings.SHARE_ROOT))
        self.assertTrue(os.path.exists(settings.SHARE_ROOT))
        self.assertTrue(os.path.isdir(settings.SHARE_ROOT))

        # Path should be written POSIX style to avoid display issues
        path_posix = posixpath.normpath(settings.SHARE_ROOT)
        self.assertTrue(settings.SHARE_ROOT == path_posix)
        