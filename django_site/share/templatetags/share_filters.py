from django import template

register = template.Library()

@register.filter
def print_size(value):
    if value < 1000:
        result = '{0}   '.format(value) + '  o'
    elif value < 1000 ** 2:
        result = '{0:.2f}'.format(value / 1000) + ' Ko'
    elif value < 1000 ** 3:
        result = '{0:.2f}'.format(value / 1000 ** 2) + ' Mo'
    elif value < 1000 ** 4:
        result = '{0:.2f}'.format(value / 1000 ** 3) + ' Go'
    else:
        result = '{0:.2f}'.format(value / 1000 ** 4) + ' To'
    
    return result
