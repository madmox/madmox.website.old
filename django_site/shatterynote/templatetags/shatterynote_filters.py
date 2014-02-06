from django import template
from django.utils import timezone

register = template.Library()

def pluralize(value, plural_mark='s'):
    if value > 1:
        return plural_mark
    else:
        return ''

@register.filter
def days_until(value):
    delta = value - timezone.now()
    days = delta.days
    hours = delta.seconds // 3600
    
    if days > 0 and hours == 0:
        result = '{0} jour{1}'.format(days, pluralize(days))
    elif days > 0 and hours > 0:
        result = (
            '{0} jour{1}, {2} heure{3}'.format(
                days,
                pluralize(days),
                hours,
                pluralize(hours)
            )
        )
    else:
        result = '{0} heure{1}'.format(hours, pluralize(hours))
    
    return result
