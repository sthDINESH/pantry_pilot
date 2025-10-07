from django import forms
from .models import ShoppingList, ShoppingListItem


class ShoppingListForm(forms.ModelForm):
    """
    Form for adding a single shopping list
    related to :model:`ShoppingList`
    """
    class Meta:
        model = ShoppingList
        fields = (
            'week_start_date',
            'week_end_date',
        )
        widgets = {
            'week_start_date': forms.HiddenInput(),
            'week_end_date': forms.HiddenInput(),
        }


class ShoppingListItemForm(forms.ModelForm):
    """
    Form for adding single shopping list item
    related to :model:`ShoppingListItem`
    """
    class Meta:
        model = ShoppingListItem
        fields = (
            'item_name',
            'quantity',
            'units',
            'notes',
        )
