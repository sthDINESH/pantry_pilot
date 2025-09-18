from django.shortcuts import render
from django.views.generic import ListView
from .models import PantryItem

# Create your views here.


class PantryItemList(ListView):
    """
    """
    context_object_name = 'pantry_items'  # Renames object_list to pantry_items
    queryset = PantryItem.objects.all()
    template_name = 'pantry/pantry_item_list.html'
