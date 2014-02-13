from django import template
from django.core.urlresolvers import reverse
from core.navigation import NavigationNode
from recipes.models import Category

register = template.Library()


@register.assignment_tag(takes_context=True)
def set_recipes_navigation(context, current_path):
    """Returns a list of NavigationNode instances containing informations
    to build the navigation specific to this app
    """
    results = []
    categories = Category.objects.all().order_by('order')
    current_recipe = context.get('recipe', None)
    
    for category in categories:
        url = reverse('recipes:category', args=(category.pk, category.slug,))
        label = category.name
        active = (current_path == url) or (
            current_recipe != None and (
                current_recipe.category.pk == category.pk
            )
        )
        results.append(NavigationNode(active, url, label))
    
    return results
