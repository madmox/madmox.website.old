from django.shortcuts import render
from recipes.models import Category


def index(request):
    categories = Category.objects.all().order_by('order')
    return render(request, 'recipes/index.html', {'categories': categories})

def category(request, category_id):
    return render(request, 'recipes/category.html', {})

def detail(request, recipe_id):
    return render(request, 'recipes/detail.html', {})
