from django.contrib import admin
from .models import MealPlanItem


@admin.register(MealPlanItem)
class MealPlanItemAdmin(admin.ModelAdmin):
    """
    Admin class related to :model:`MealPlanItem`
    """
    list_display = (
        'user',
        'recipe',
        'meal_type',
        'date'
    )
    list_filter = (
        'user',
        'date',
        'meal_type',
    )
