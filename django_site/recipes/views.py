from django.shortcuts import render, get_object_or_404
from recipes.models import Category, Recipe


def index(request):
    categories = Category.objects.all().order_by('order')
    return render(request, 'recipes/index.html', {'categories': categories})

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'recipes/category.html', {'category': category})

def detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, 'recipes/detail.html', {'recipe': recipe})
