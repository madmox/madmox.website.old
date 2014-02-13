from django.contrib import admin
from recipes.models import Category, Recipe, Tool, Ingredient, Step


class CategoryAdmin(admin.ModelAdmin):
    pass


class ToolInline(admin.TabularInline):
    model = Tool
    extra = 1
    ordering = ('order',)


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1
    ordering = ('order',)


class StepInline(admin.TabularInline):
    model = Step
    extra = 1
    ordering = ('order',)

    
class RecipeAdmin(admin.ModelAdmin):
    inlines = [ToolInline, IngredientInline, StepInline]

    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
