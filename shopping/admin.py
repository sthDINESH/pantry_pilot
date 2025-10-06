from django.contrib import admin
from .models import ShoppingList, ShoppingListItem


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ["week_start_date", "week_end_date", "user", "created_on"]
    list_filter = ["user", "created_on", "updated_on"]


@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = [
        "item_name",
        "quantity",
        "units",
        "shopping_list",
        "created_on",
    ]
    list_filter = ["shopping_list"]
