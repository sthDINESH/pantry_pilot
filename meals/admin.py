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
        'start_time',
        'end_time',
    )
    list_filter = (
        'user',
        'start_time',
        'meal_type',
    )
