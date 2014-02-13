from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template import Template, Context
from recipes.tests.common import *


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
            [repr(category)]
        )
        self.assertContains(response, category.name, status_code=200)


class CategoryViewTests(TestCase):

    def test_category_view_404(self):
        """
        Tests the view returns a 404 HTTP status code if an unknown ID is given
        """
        response = self.client.get(
            reverse('recipes:category', args=(1, 'wrong-slug',))
        )
        self.assertEqual(response.status_code, 404)
        
    def test_category_view_wrong_slug(self):
        """
        Tests the view returns a redirect status code if valid ID is given
        but wrong slug
        """
        category = create_category('Nouvelle catégorie', 1)
        response = self.client.get(
            reverse('recipes:category', args=(category.pk, 'wrong-slug',)),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.redirect_chain)
        self.assertEqual(len(response.redirect_chain), 1)
        try:
            ctx_category = response.context['category']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        self.assertEqual(category, ctx_category)
        
    def test_category_view_exists(self):
        """
        Tests the view returns a 200 HTTP status code if a good ID is given
        """
        category = create_category('Nouvelle catégorie', 1)
        response = self.client.get(
            reverse('recipes:category', args=(category.pk, category.slug,))
        )
        self.assertEqual(response.status_code, 200)
        try:
            ctx_category = response.context['category']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        self.assertEqual(category, ctx_category)
        
    def test_category_view_with_recipe(self):
        """
        Tests the view displays a recipe whose category is the one requested
        """
        category1 = create_category('Nouvelle catégorie 1', 1)
        category2 = create_category('Nouvelle catégorie 2', 2)
        recipe1 = create_recipe('Recipe 1', category1)
        response = self.client.get(
            reverse('recipes:category', args=(category1.pk, category1.slug,))
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
            reverse('recipes:category', args=(category2.pk, category2.slug,))
        )
        self.assertNotContains(response, recipe1.name, status_code=200)


class DetailViewTests(TestCase):

    def test_recipe_view_404(self):
        """
        Tests the view returns a 404 HTTP status code if an unknown ID is given
        """
        response = self.client.get(
            reverse('recipes:detail', args=(1, 'unknown-slug',))
        )
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_view_wrong_slug(self):
        """
        Tests the view returns a redirect status code if valid ID is given
        but wrong slug
        """
        category = create_category('Nouvelle catégorie', 1)
        recipe = create_recipe('Recette', category)
        response = self.client.get(
            reverse('recipes:detail', args=(recipe.pk, 'wrong-slug',)),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.redirect_chain)
        self.assertEqual(len(response.redirect_chain), 1)
        try:
            ctx_recipe = response.context['recipe']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        self.assertEqual(recipe, ctx_recipe)
        
    def test_recipe_view_exists(self):
        """
        Tests the view returns a 200 HTTP status code if a good ID is given
        """
        category = create_category('Nouvelle catégorie', 1)
        recipe = create_recipe('Recette', category)
        response = self.client.get(
            reverse('recipes:detail', args=(recipe.pk, recipe.slug,))
        )
        self.assertContains(response, recipe.name, status_code=200)
        try:
            ctx_recipe = response.context['recipe']
        except KeyError as ke:
            self.fail("context does not contain key {0}".format(str(ke)))
        self.assertEqual(recipe, ctx_recipe)


class RecipesNavigationTests(TestCase):
    def setUp(self):
        self.category = create_category('Catégorie 1', 1)
        self.template = Template(
            '{% load recipes_navigation %}'
            '{% set_recipes_navigation current_path as results %}'
        )

    def test_set_recipes_navigation(self):
        url = reverse(
            'recipes:category',
            args=(self.category.pk, self.category.slug,)
        )
        c = Context({"current_path": url})
        rendered = self.template.render(c)
        self.assertIsInstance(c['results'], list)
        self.assertEqual(len(c['results']), 1)
        self.assertEqual(c['results'][0].url, url)
