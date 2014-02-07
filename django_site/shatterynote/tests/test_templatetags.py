from django.test import TestCase
from django.template import Template, Context
from django.utils import timezone


class ShatteryNoteFiltersTests(TestCase):

    def setUp(self):
        self.template = Template(
            '{% load shatterynote_filters %}'
            '{{ expires|days_until }}'
        )

    def test_days_until_days_hours(self):
        """
        Tests the days_until filter works properly when it should display
        a days+hours like result
        """
        expires = timezone.now() + timezone.timedelta(days=6, seconds=3700)
        c = Context({"expires": expires})
        rendered = self.template.render(c)
        self.assertEqual(rendered, '6 jours, 1 heure')

    def test_days_until_days_only(self):
        """
        Tests the days_until filter works properly when it should display
        a days+hours like result
        """
        expires = timezone.now() + timezone.timedelta(days=6, seconds=100)
        c = Context({"expires": expires})
        rendered = self.template.render(c)
        self.assertEqual(rendered, '6 jours')

    def test_days_until_hours_only(self):
        """
        Tests the days_until filter works properly when it should display
        a days+hours like result
        """
        expires = timezone.now() + timezone.timedelta(days=0, seconds=3700)
        c = Context({"expires": expires})
        rendered = self.template.render(c)
        self.assertEqual(rendered, '1 heure')
