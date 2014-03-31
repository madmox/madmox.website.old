from django import template
from django.core.urlresolvers import reverse
from core.navigation import NavigationNode

import urllib.parse

register = template.Library()


@register.assignment_tag
def set_about_navigation(current_path):
    """Returns a list of NavigationNode instances containing informations
    to build the navigation specific to this app
    """
    results = []
    
    url = reverse('about:index')
    label = 'A propos'
    active = (urllib.parse.unquote(current_path) == urllib.parse.unquote(url))
    results.append(NavigationNode(active, url, label))
    
    url = reverse('about:cv')
    label = 'Mon C.V.'
    active = (current_path == url)
    results.append(NavigationNode(active, url, label))
    
    return results
