from django import template
from django.core.urlresolvers import reverse

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
    
    path, isdir, isfile = get_physical_path('')
    node = FileSystemNode(path)
    
    for child in node.children:
        url = reverse('share:browse', args=(child.url,))
        label = child.name
        active = current_path.startswith(url)
        results.append(NavigationNode(active, url, label))
    
    return results
