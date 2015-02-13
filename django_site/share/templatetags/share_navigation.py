from django import template
from django.core.urlresolvers import reverse

import urllib.parse

from core.navigation import NavigationNode
from share.utils import (
    get_physical_path,
    FileSystemNode
)

register = template.Library()


@register.assignment_tag(takes_context=True)
def set_share_navigation(context, current_path):
    """Returns a list of NavigationNode instances containing informations
    to build the navigation specific to this app
    """
    results = []
    
    filepath = get_physical_path('')
    node = FileSystemNode(filepath)
    
    for child in node.children:
        url = reverse('share:browse', args=(child.url,))
        label = child.name
        unquoted_curpath = urllib.parse.unquote(current_path)
        unquoted_url = urllib.parse.unquote(url)
        active = unquoted_curpath.startswith(unquoted_url)
        results.append(NavigationNode(active, url, label))
    
    return results
