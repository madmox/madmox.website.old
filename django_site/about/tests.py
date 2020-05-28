from django.test import TestCase
from django.core.urlresolvers import reverse
from about.templatetags.about_navigation import set_about_navigation
from core.navigation import NavigationNode


class AboutIndexTests(TestCase):
    def test_index_view(self):
        """
        Tests the view returns a 200 HTTP code
        """
        response = self.client.get(reverse('about:index'))
        self.assertEqual(response.status_code, 200)


class AboutNavigationTests(TestCase):
    def test_navigation_list(self):
        nav = set_about_navigation(reverse('about:index'))
        self.assertIsInstance(nav, list)
        
    def test_navigation_contains(self):
        nav = set_about_navigation(reverse('about:index'))
        try:
            index = next(x for x in nav if x.url == reverse('about:index'))
        except StopIteration:
            self.fail('Could not find index entry in navigation')
        self.assertTrue(index.active)
