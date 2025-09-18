from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PantryItem

# Create your views here.


class PantryItemList(LoginRequiredMixin, ListView):
    """
    Display pantry items for the currently logged-in user
    """
    context_object_name = 'pantry_items'
    template_name = 'pantry/pantry_item_list.html'
    
    def get_queryset(self):
        """
        Filter pantry items to only show items belonging to the current user
        """
        return PantryItem.objects.filter(user=self.request.user)
