from django.contrib import admin
from .models import PantryItem, Category

# Register your models here.


@admin.register(PantryItem)
class PantryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'user', 'updated_on')
    list_filter = ('user', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'user', 'created_on')
    list_filter = ('user', 'category_name')
