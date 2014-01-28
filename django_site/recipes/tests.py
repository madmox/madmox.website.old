from django.test import TestCase
from django.core.urlresolvers import reverse
from recipes.models import Category, Recipe, Tool, Ingredient, Step


def create_category(name, order):
    """
    Creates a new category
    """
    category = Category()
    category.name = name
    category.order = order
    category.save()
    return category
    
    
def create_recipe(
    name, category, nb_persons=1,
    preparation_time=2, total_time=2
):
    """
    Creates a new recipe
    """
    recipe = Recipe()
    recipe.name = name
    recipe.category = category
    recipe.nb_persons = nb_persons
    recipe.preparation_time = preparation_time
    recipe.total_time = total_time
    recipe.save()
    return recipe


def create_tool(label, order, recipe):
    tool = Tool()
    tool.label = label
    tool.order = order
    tool.recipe = recipe
    tool.save()
    return tool


def create_ingredient(label, order, recipe):
    ingredient = Ingredient()
    ingredient.label = label
    ingredient.order = order
    ingredient.recipe = recipe
    ingredient.save()
    return ingredient


def create_step(label, order, recipe):
    step = Step()
    step.label = label
    step.order = order
    step.recipe = recipe
    step.save()
    return step


class IndexViewTests(TestCase):
    def test_index_view(self):
        """
        Tests the view returns a 200 HTTP code
        """
        response = self.client.get(reverse('recipes:index'))
        self.assertEqual(response.status_code, 200)
        
    def test_index_view_no_category(self):
        """
        Tests the view returns a 200 HTTP code and contains no category
        """
        response = self.client.get(reverse('recipes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['categories'], [])
        
    def test_index_view_with_category(self):
        """
        Tests the view returns a 200 HTTP code and contains the new category
        """
        category = create_category('Nouvelle catégorie', 1)
        response = self.client.get(reverse('recipes:index'))
        self.assertQuerysetEqual(
            response.context['categories'],
            [category.__repr__()]
        )
        self.assertContains(response, category.name, status_code=200)


class CategoryViewTests(TestCase):
    def test_category_view_404(self):
        """
        Tests the view returns a 404 HTTP status code if an unknown ID is given
        """
        response = self.client.get(reverse('recipes:category', args=(0,)))
        self.assertEqual(response.status_code, 404)
        
    def test_category_view_exists(self):
        """
        Tests the view returns a 200 HTTP status code if a good ID is given
        """
        category = create_category('Nouvelle catégorie', 1)
        response = self.client.get(
            reverse('recipes:category', args=(category.pk,))
        )
        self.assertEqual(response.status_code, 200)
        
    def test_category_view_with_recipe(self):
        """
        Tests the view displays a recipe whose category is the one requested
        """
        category1 = create_category('Nouvelle catégorie 1', 1)
        category2 = create_category('Nouvelle catégorie 2', 2)
        recipe1 = create_recipe('Recipe 1', category1)
        response = self.client.get(
            reverse('recipes:category', args=(category1.pk,))
        )
        self.assertContains(response, recipe1.name, status_code=200)
        
    def test_category_view_with_other_recipe(self):
        """
        Tests the view displays a recipe whose category is the one requested
        """
        category1 = create_category('Nouvelle catégorie 1', 1)
        category2 = create_category('Nouvelle catégorie 2', 2)
        recipe1 = create_recipe('Recipe 1', category1)
        response = self.client.get(
            reverse('recipes:category', args=(category2.pk,))
        )
        self.assertNotContains(response, recipe1.name, status_code=200)


class DetailViewTests(TestCase):
    def test_recipe_view_404(self):
        """
        Tests the view returns a 404 HTTP status code if an unknown ID is given
        """
        response = self.client.get(reverse('recipes:detail', args=(0,)))
        self.assertEqual(response.status_code, 404)
        
    def test_category_view_exists(self):
        """
        Tests the view returns a 200 HTTP status code if a good ID is given
        """
        category = create_category('Nouvelle catégorie', 1)
        recipe = create_recipe('Recette', category)
        response = self.client.get(
            reverse('recipes:detail', args=(recipe.pk,))
        )
        self.assertContains(response, recipe.name, status_code=200)


class CategoryModelTests(TestCase):
    def test_create_category(self):
        """
        Asserts category gets created successfully
        """
        category = create_category('Catégorie 1', 1)
        self.assertNotEqual(category.pk, None)


class RecipeModelTests(TestCase):
    def test_create_recipe(self):
        """
        Asserts recipe gets created successfully
        """
        category = create_category('Catégorie 1', 1)
        recipe = create_recipe('Recette 1', category, 1, 2, 2)
        self.assertNotEqual(recipe.pk, None)


class ToolModelTests(TestCase):
    def test_create_tool(self):
        """
        Asserts tool gets created successfully
        """
        category = create_category('Catégorie 1', 1)
        recipe = create_recipe('Recette 1', category, 1, 2, 2)
        tool = create_tool('Ustensile 1', 1, recipe)
        self.assertNotEqual(tool.pk, None)


class IngredientModelTests(TestCase):
    def test_create_ingredient(self):
        """
        Asserts ingredient gets created successfully
        """
        category = create_category('Catégorie 1', 1)
        recipe = create_recipe('Recette 1', category, 1, 2, 2)
        ingredient = create_ingredient('Ingrédient 1', 1, recipe)
        self.assertNotEqual(ingredient.pk, None)


class StepModelTests(TestCase):
    def test_create_step(self):
        """
        Asserts step gets created successfully
        """
        category = create_category('Catégorie 1', 1)
        recipe = create_recipe('Recette 1', category, 1, 2, 2)
        step = create_step('Etape 1', 1, recipe)
        self.assertNotEqual(step.pk, None)
