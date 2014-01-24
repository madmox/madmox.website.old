from django.shortcuts import render, get_object_or_404
from recipes.models import Category, Recipe


def index(request):
    categories = Category.objects.all().order_by('order')
    return render(request, 'recipes/index.html', {'categories': categories})

def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, 'recipes/category.html', {'category': category})

def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'recipes/detail.html', {'recipe': recipe})
