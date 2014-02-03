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
