from django.db import models
from django.core.validators import MinValueValidator


# Models
class Category(models.Model):
    """Each recipe as one and only one category
    
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
    
    class Meta():
        verbose_name = "catégorie"
    
    def __str__(self):
        return self.name
    
    def ordered_recipes(self):
        return self.recipe_set.all().order_by('name')


class Recipe(models.Model):
    """Represents a recipe as displayed on each recipe's page
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
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="date de création"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="date de mise à jour"
    )
    image = models.ImageField(
        upload_to='recipes/recipes/',
        blank=True,
        verbose_name="image"
    )
    
    class Meta():
        verbose_name = "recette"
    
    def __str__(self):
        return self.name


class Tool(models.Model):
    """A recipe tool
    """
    
    label = models.CharField(max_length=100, verbose_name="nom")
    recipe = models.ForeignKey(Recipe, verbose_name="recette")
    
    class Meta():
        verbose_name = "ustensile"
    
    def __str__(self):
        return self.label


class Ingredient(models.Model):
    """A recipe ingredient
    """
    
    label = models.CharField(max_length=100, verbose_name="nom")
    recipe = models.ForeignKey(Recipe, verbose_name="recette")
    
    class Meta():
        verbose_name = "ingrédient"
    
    def __str__(self):
        return self.label


class Step(models.Model):
    """A recipe step
    """
    
    label = models.CharField(max_length=200, verbose_name="libellé")
    recipe = models.ForeignKey(Recipe, verbose_name="recette")
    
    class Meta():
        verbose_name = "étape"
    
    def __str__(self):
        return self.label
