from django.db import models
from django.core.validators import MinValueValidator
from django.template.defaultfilters import slugify


# Models
class Category(models.Model):
    """
    Each recipe has one and only one category
    It is used to classify recipes in groups to facilitate search operations
    """
    
    name = models.CharField(max_length=50, verbose_name="nom")
    order = models.IntegerField(
        validators=[MinValueValidator(0)],
        unique=True,
        verbose_name="ordre d'affichage"
    )
    image = models.ImageField(
        upload_to='recipes/categories/',
        blank=True,
        verbose_name="image"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="date de mise à jour"
    )
    
    @property
    def slug(self):
        return slugify(self.name)
    
    class Meta():
        verbose_name = "catégorie"
    
    def __str__(self):
        return self.name
    
    def ordered_recipes(self):
        return self.recipe_set.all().order_by('name')


class Recipe(models.Model):
    """
    Represents a recipe as displayed on each recipe's page
    """
    
    name = models.CharField(max_length=50, verbose_name="nom")
    category = models.ForeignKey(Category, verbose_name="catégorie")
    nb_persons = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="nombre de personnes"
    )
    preparation_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="temps de préparation (en minutes)"
    )
    total_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="temps total (en minutes)"
    )
    image = models.ImageField(
        upload_to='recipes/recipes/',
        blank=True,
        verbose_name="image"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="date de mise à jour"
    )
    
    @property
    def slug(self):
        return slugify(self.name)
    
    class Meta():
        verbose_name = "recette"
    
    def __str__(self):
        return self.name
    
    def ordered_tools(self):
        return self.tool_set.all().order_by('order')
    
    def ordered_ingredients(self):
        return self.ingredient_set.all().order_by('order')
    
    def ordered_steps(self):
        return self.step_set.all().order_by('order')


class Tool(models.Model):
    """
    A recipe tool
    """
    
    label = models.CharField(max_length=100, verbose_name="nom")
    order = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="ordre d'affichage"
    )
    recipe = models.ForeignKey(Recipe, verbose_name="recette")
    
    class Meta():
        verbose_name = "ustensile"
        unique_together = (('recipe', 'order'),)
    
    def __str__(self):
        return self.label


class Ingredient(models.Model):
    """
    A recipe ingredient
    """
    
    label = models.CharField(max_length=100, verbose_name="nom")
    order = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="ordre d'affichage"
    )
    recipe = models.ForeignKey(Recipe, verbose_name="recette")
    
    class Meta():
        verbose_name = "ingrédient"
        unique_together = (('recipe', 'order'),)
    
    def __str__(self):
        return self.label


class Step(models.Model):
    """
    A recipe step
    """
    
    label = models.CharField(max_length=200, verbose_name="libellé")
    order = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="ordre d'affichage"
    )
    recipe = models.ForeignKey(Recipe, verbose_name="recette")
    
    class Meta():
        verbose_name = "étape"
        unique_together = (('recipe', 'order'),)
    
    def __str__(self):
        return self.label
