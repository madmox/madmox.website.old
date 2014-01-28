from django.test import TestCase
from django.core.urlresolvers import reverse


class AboutIndexTests(TestCase):
    def test_index_view(self):
        """
        Tests the view returns a 200 HTTP code
        """
        response = self.client.get(reverse('about:index'))
        self.assertEqual(response.status_code, 200)


class AboutCvTests(TestCase):
    def test_cv_view(self):
        """
        Tests the view returns a 200 HTTP code
        """
        response = self.client.get(reverse('about:cv'))
        self.assertEqual(response.status_code, 200)
