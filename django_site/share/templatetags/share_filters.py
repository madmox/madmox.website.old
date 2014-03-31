from django import template

register = template.Library()

@register.filter
def print_size(value):
    if value < 1024:
        result = '{0}   '.format(value) + '  o'
    elif value < 1024 ** 2:
        result = '{0:.2f}'.format(value / 1024) + ' Ko'
    elif value < 1024 ** 3:
        result = '{0:.2f}'.format(value / 1024 ** 2) + ' Mo'
    elif value < 1024 ** 4:
        result = '{0:.2f}'.format(value / 1024 ** 3) + ' Go'
    else:
        result = '{0:.2f}'.format(value / 1024 ** 4) + ' To'
    
    return result
