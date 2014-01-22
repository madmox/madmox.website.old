from django.contrib import admin
from recipes.models import Category, Recipe, Tool, Ingredient, Step


class ToolInline(admin.TabularInline):
    model = Tool
    extra = 1


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class StepInline(admin.TabularInline):
    model = Step
    extra = 1

    
class RecipeAdmin(admin.ModelAdmin):
    inlines = [ToolInline, IngredientInline, StepInline]

    
admin.site.register(Category)
admin.site.register(Recipe, RecipeAdmin)
