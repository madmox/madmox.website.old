from django.test import TestCase
from django.template import Template, Context


class RecipesFiltersTests(TestCase):
    def setUp(self):
        self.template = Template(
            '{% load recipes_filters %}'
            '{{ minutes|display_minutes }}'
        )

    def test_display_hours_only(self):
        """
        Tests the display_minutes filter works properly when it should display
        a HHh like result
        """
        c = Context({"minutes": 182})
        rendered = self.template.render(c)
        self.assertEqual(rendered, '3h02')
        
    def test_display_hours_minutes(self):
        """
        Tests the display_minutes filter works properly when it should display
        a HHhMM like result
        """
        c = Context({"minutes": 180})
        rendered = self.template.render(c)
        self.assertEqual(rendered, '3h')
        
    def test_display_minute(self):
        """
        Tests the display_minutes filter works properly when it should display
        a result containing only 1 minute
        """
        c = Context({"minutes": 1})
        rendered = self.template.render(c)
        self.assertEqual(rendered, '1 minute')
        
    def test_display_minutes_only(self):
        """
        Tests the display_minutes filter works properly when it should display
        a result containing only minutes
        """
        c = Context({"minutes": 50})
        rendered = self.template.render(c)
        self.assertEqual(rendered, '50 minutes')
