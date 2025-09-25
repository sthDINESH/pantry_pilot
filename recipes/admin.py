from django.contrib import admin
from .models import SavedRecipe, RecipeIngredient

# Register your models here.


@admin.register(SavedRecipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ('title', 'user')
    list_filter = ("user", "status", "created_on")
    prepopulated_fields = {'slug': ('title',)}


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient_name',
        'quantity',
        'units',
        'recipe_id',
        'created_on'
    )
    list_filter = ('recipe_id',)
