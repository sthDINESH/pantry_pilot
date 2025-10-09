from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import config.constants as constants


class Category(models.Model):
    """
    Stores a single category related to :model:`auth.User`
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="categories"
    )
    category_name = models.CharField(
        "Category",
        max_length=20, choices=constants.CATEGORY_CHOICES, default='other'
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_category_name_display()}"

    class Meta:
        unique_together = ['user', 'category_name']
        ordering = ['category_name']


class PantryItem(models.Model):
    """
    Stores a single pantry item with quantity and units
    related to :model:`auth.User` and :model:`Category`
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pantry_items"
    )
    name = models.CharField("Item", max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.CharField(
        max_length=20, choices=constants.UNIT_CHOICES, default='piece'
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="pantry_items"
    )
    image = CloudinaryField('image', default="placeholder", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.get_units_display()})"

    class Meta:
        unique_together = ['user', 'name']
        ordering = ['name']
