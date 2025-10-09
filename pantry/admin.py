from django.contrib import admin
from .models import PantryItem, Category


@admin.register(PantryItem)
class PantryItemAdmin(admin.ModelAdmin):
    """
    ModelAdmin class related to :model:`PantryItem`
    """
    list_display = ('name', 'category', 'user', 'updated_on')
    list_filter = ('user', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    ModelAdmin class related to :model:`Category`
    """
    list_display = ('category_name', 'user', 'created_on')
    list_filter = ('user', 'category_name')
