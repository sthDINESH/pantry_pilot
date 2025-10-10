from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from recipes.models import SavedRecipe
import config.constants as constants


class MealPlanItem(models.Model):
    """
    Stores a single Meal plan item
    related to :model:`auth.user` and :model:`SavedRecipe`
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="meal_plan_items",
    )
    recipe = models.ForeignKey(
        SavedRecipe,
        on_delete=models.CASCADE,
        related_name="meal_plan",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    meal_type = models.CharField(
        max_length=20,
        choices=constants.MEAL_PLAN_CATEGORIES,
        default="other",
    )
    servings = models.IntegerField(
        validators=[MinValueValidator(1)],  # Minimum value is 1
        default=1
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}-{self.recipe}:{self.meal_type}"

    class Meta:
        unique_together = ['user', 'recipe', 'start_time']
        ordering = ['recipe', '-created_on']
