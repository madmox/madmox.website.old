from django import template
from django.core.urlresolvers import reverse
from core.navigation import NavigationNode

register = template.Library()


@register.assignment_tag(takes_context=True)
def set_shatterynote_navigation(context, current_path):
    """Returns a list of NavigationNode instances containing informations
    to build the navigation specific to this app
    """
    results = []
    url = reverse('shatterynote:index')
    active = current_path.startswith(url)
    label = 'Partager un secret'
    results.append(NavigationNode(active, url, label))
    
    return results
