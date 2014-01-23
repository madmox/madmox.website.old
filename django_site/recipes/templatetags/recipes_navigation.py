from django import template
from django.core.urlresolvers import reverse
from core.navigation import NavigationNode
from recipes.models import Category

register = template.Library()


@register.assignment_tag
def set_recipes_navigation(current_path):
    """Returns a list of NavigationNode instances containing informations
    to build the navigation specific to this app
    """
    results = []
    categories = Category.objects.all().order_by('order')
    
    for category in categories:
        url = reverse('recipes:category', args=(category.id,))
        label = category.name
        active = (current_path == url)
        results.append(NavigationNode(active, url, label))
    
    return results
