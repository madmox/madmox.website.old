from django import template

register = template.Library()


@register.simple_tag
def nav_active(current_path, navigation_pattern):
    """Returns the CSS class of a navigation entry given the current request
    path (i.e. 'active' if the U.R.L. matches the navigation pattern, else an
    empty string)
    """
    if current_path.startswith(navigation_pattern):
        return 'active'
    else:
        return ''
