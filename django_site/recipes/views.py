from django.shortcuts import render, get_object_or_404
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from recipes.models import Category, Recipe


def index(request):
    categories = Category.objects.all().order_by('order')
    return render(request, 'recipes/index.html', {'categories': categories})

def category(request, id, slug):
    category = get_object_or_404(Category, pk=id)
    if category.slug != slug:
        return HttpResponsePermanentRedirect(
            reverse('recipes:category', args=(category.pk, category.slug,))
        )
    return render(request, 'recipes/category.html', {'category': category})

def detail(request, id, slug):
    recipe = get_object_or_404(Recipe, pk=id)
    if recipe.slug != slug:
        return HttpResponsePermanentRedirect(
            reverse('recipes:detail', args=(recipe.pk, recipe.slug,))
        )
    return render(request, 'recipes/detail.html', {'recipe': recipe})
