from django.db import models
from django.contrib.auth.models import User
import config.constants as constants


class ShoppingList(models.Model):
    """
    Stores a single shopping list related to :model:`auth.User`
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_lists"
    )
    week_start_date = models.DateField()
    week_end_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Week: {self.week_start_date} - {self.week_end_date}, User: {self.user}"

    class Meta:
        unique_together = ["user", "week_start_date"]
        ordering = ["-created_on"]


class ShoppingListItem(models.Model):
    """
    Stores a single shopping list item
    related to :model:`ShoppingList` and :model:`Category`
    """
    shopping_list = models.ForeignKey(
        ShoppingList,
        on_delete=models.CASCADE,
        related_name="shopping_list_items",
    )
    item_name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.CharField(
        max_length=20,
        choices=constants.UNIT_CHOICES,
        default='piece',
    )
    notes = models.TextField(default="", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_name} - {self.quantity} {self.get_units_display()}"

    class Meta:
        ordering = ["-created_on"]
