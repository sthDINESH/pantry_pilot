from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


class Category(models.Model):
    """
    Stores a single category related to :model:`auth.User`
    """
    CATEGORY_CHOICES = [
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('grains', 'Grains'),
        ('proteins', 'Proteins'),
        ('dairy', 'Dairy'),
        ('spices', 'Spices & Seasonings'),
        ('condiments', 'Condiments & Sauces'),
        ('oils', 'Oils & Vinegars'),
        ('canned', 'Canned Goods'),
        ('frozen', 'Frozen Items'),
        ('snacks', 'Snacks'),
        ('beverages', 'Beverages'),
        ('baking', 'Baking Supplies'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="categories"
    )
    category_name = models.CharField(
        "Category",
        max_length=20, choices=CATEGORY_CHOICES, default='other'
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_category_name_display()}"

    class Meta:
        unique_together = ['user', 'category_name']
        ordering = ['-created_on']


class PantryItem(models.Model):
    """
    Stores a single pantry item with quantity and units
    related to :model:`auth.User` and :model:`Category`
    """
    UNIT_CHOICES = [
        # Weight measurements
        ('kg', 'Kilograms'),
        ('g', 'Grams'),
        ('lb', 'Pounds'),
        ('oz', 'Ounces'),

        # Volume measurements - Metric
        ('l', 'Liters'),
        ('ml', 'Milliliters'),

        # Volume measurements - Imperial/US
        ('cup', 'Cups'),
        ('tbsp', 'Tablespoons'),
        ('tsp', 'Teaspoons'),
        ('fl_oz', 'Fluid Ounces'),
        ('pt', 'Pints'),
        ('qt', 'Quarts'),
        ('gal', 'Gallons'),

        # Count/Piece measurements
        ('piece', 'Pieces'),
        ('item', 'Items'),
        ('can', 'Cans'),
        ('bottle', 'Bottles'),
        ('jar', 'Jars'),
        ('bag', 'Bags'),
        ('box', 'Boxes'),
        ('pack', 'Packs'),
        ('bunch', 'Bunches'),
        ('head', 'Heads'),
        ('clove', 'Cloves'),
        ('slice', 'Slices'),

        # Special measurements
        ('pinch', 'Pinches'),
        ('dash', 'Dashes'),
        ('drop', 'Drops'),
        ('serving', 'Servings'),
        ('portion', 'Portions'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pantry_items"
    )
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.CharField(
        max_length=20, choices=UNIT_CHOICES, default='piece'
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="pantry_items"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.get_units_display()})"

    def clean(self):
        """
        Validates that the category belongs to the same user as the pantry item
        """
        super().clean()
        # Check if both user and category are set
        # if self.category and self.category.user != self.user:
        #     raise ValidationError({
        #         'category': 'Category must belong to the same user '
        #                     'as the pantry item.'
        #     })

    def save(self, *args, **kwargs):
        """
        Override save to ensure validation runs every time
        """
        self.full_clean()  # This calls clean() and validates all fields
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['user', 'name']
        ordering = ['name']
