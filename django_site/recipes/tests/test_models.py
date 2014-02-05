from django.test import TestCase
from recipes.tests.common import *


class CategoryModelTests(TestCase):
    def test_create_category(self):
        """
        Asserts category gets created successfully
        """
        category = create_category('Catégorie 1', 1)
        self.assertIsNotNone(category.pk)


class RecipeModelTests(TestCase):
    def test_create_recipe(self):
        """
        Asserts recipe gets created successfully
        """
        category = create_category('Catégorie 1', 1)
        recipe = create_recipe('Recette 1', category, 1, 2, 2)
        self.assertIsNotNone(recipe.pk)


class ToolModelTests(TestCase):
    def test_create_tool(self):
        """
        Asserts tool gets created successfully
        """
        category = create_category('Catégorie 1', 1)
        recipe = create_recipe('Recette 1', category, 1, 2, 2)
        tool = create_tool('Ustensile 1', 1, recipe)
        self.assertIsNotNone(tool.pk)


class IngredientModelTests(TestCase):
    def test_create_ingredient(self):
        """
        Asserts ingredient gets created successfully
        """
        category = create_category('Catégorie 1', 1)
        recipe = create_recipe('Recette 1', category, 1, 2, 2)
        ingredient = create_ingredient('Ingrédient 1', 1, recipe)
        self.assertIsNotNone(ingredient.pk)


class StepModelTests(TestCase):
    def test_create_step(self):
        """
        Asserts step gets created successfully
        """
        category = create_category('Catégorie 1', 1)
        recipe = create_recipe('Recette 1', category, 1, 2, 2)
        step = create_step('Etape 1', 1, recipe)
        self.assertIsNotNone(step.pk)
