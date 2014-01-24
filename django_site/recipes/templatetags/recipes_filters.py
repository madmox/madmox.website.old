from django import template

register = template.Library()

@register.filter
def display_minutes(value):
    hours = value // 60
    minutes = value % 60
    if hours > 0:
        if (minutes > 0):
            result = '{0}h{1}'.format(hours, minutes)
        else:
            result = '{0}h'.format(hours)
    else:
        result = '{0} minutes'.format(minutes)
    return result
