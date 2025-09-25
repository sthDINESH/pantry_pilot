from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import config.constants as constants


# Create your models here.

class SavedRecipe(models.Model):
    """
    Stores a single recipe
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_recipes"
    )
    # Populated with Spoonacular API response details for favorited recipes
    # Default for custom recipes
    api_recipe_id = models.IntegerField("Spoonacular Recipe Id", default=0)
    api_image_url = models.URLField(default="")
    api_source_url = models.URLField(default="")
    is_external = models.BooleanField()
    # Common fields for all recipes
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField()
    prep_time = models.DecimalField(
        "Prep time",
        max_digits=10,
        decimal_places=2
    )
    prep_time_units = models.CharField(
        "Prep time units",
        max_length=10,
        choices=constants.TIME_UNIT_CHOICES,
        default="min"
    )
    cook_time = models.DecimalField(
        "Cooking time",
        max_digits=10,
        decimal_places=2
    )
    cook_time_units = models.CharField(
        "Cooking time units",
        max_length=10,
        choices=constants.TIME_UNIT_CHOICES,
        default="min"
    )
    servings = models.IntegerField()
    instructions = models.TextField()
    image = CloudinaryField('image', default="placeholder")
    notes = models.TextField(default="")
    status = models.IntegerField(choices=constants.STATUS_CHOICES, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'title', 'slug']
        ordering = ["-created_on",]

    def __str__(self):
        return f"{self.title}"


class RecipeIngredient(models.Model):
    """
    Stores a single recipe ingredient (with quantity and units)
    related to :model:`Recipe`
    """
    recipe_id = models.ForeignKey(
        SavedRecipe,
        on_delete=models.CASCADE,
        related_name=(
            "ingredients"
        )
    )
    ingredient_name = models.CharField("Ingredient", max_length=50)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.CharField(
        max_length=10,
        choices=constants.UNIT_CHOICES,
        default='piece'
    )
    notes = models.TextField(default="")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['recipe_id', 'ingredient_name']
        ordering = ['ingredient_name']

    def __str__(self):
        return f"{self.ingredient_name}"








