from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template import Template, Context


class CoreNavigationTests(TestCase):
    def setUp(self):
        self.template = Template(
            '{% load core_navigation %}'
            '{% nav_active current_path navigation_pattern %}'
        )

    def test_core_navigation_nav_active(self):
        """
        Tests the nav_active template tag returns 'active' when the pattern
        matches the current path
        """
        c = Context({
            'current_path': '/some/path/',
            'navigation_pattern': '/some/'
        })
        rendered = self.template.render(c)
        self.assertEqual(rendered, 'active')

    def test_core_navigation_nav_inactive(self):
        """
        Tests the nav_active template tag returns '' when the pattern
        does not match the current path
        """
        c = Context({
            'current_path': '/some/path/',
            'navigation_pattern': '/other/'
        })
        rendered = self.template.render(c)
        self.assertEqual(rendered, '')
