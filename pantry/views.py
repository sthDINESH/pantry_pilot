from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category

# Create your views here.


class CategoryList(LoginRequiredMixin, ListView):
    """
    Display Pantry item categories for the currently logged in user
    """
    context_object_name = "categories"
    template_name = "pantry/pantry_item_list.html"

    def get_queryset(self):
        """
        """
        return Category.objects.filter(user=self.request.user)
