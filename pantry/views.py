from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Category, PantryItem
from .forms import PantryItemForm, CategoryForm

# Create your views here.


class CategoryList(LoginRequiredMixin, ListView):
    """
    Display Pantry item categories for the currently logged in user
    """
    context_object_name = "categories"
    template_name = "pantry/pantry_category_item_list.html"

    def get_queryset(self):
        """
        """
        return Category.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pantry_item_form"] = PantryItemForm()
        context["category_form"] = CategoryForm()
        return context

    def post(self, request, *args, **kwargs):
        print("DEBUG: IN POST method")
        print(request.POST)

        category_form = CategoryForm(request.POST)
        pantry_item_form = PantryItemForm(request.POST)

        if category_form.is_valid() and pantry_item_form.is_valid():
            # Get or create a category for the user depending on
            # whether the category already exists
            category, category_created = Category.objects.get_or_create(
                user=request.user,
                category_name=category_form.cleaned_data['category_name']
            )
            if category_created:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    (
                        f"Added new category - "
                        f"{category_form.cleaned_data['category_name']}"
                    )
                )

            # Check if pantry item already exists
            item_name = pantry_item_form.cleaned_data['name']
            existing_item = PantryItem.objects.filter(
                user=request.user,
                name=item_name,
            ).first()

            if existing_item:
                # TODO pass for now
                messages.add_message(
                    request,
                    messages.WARNING,
                    f"Item already exists - {pantry_item_form.cleaned_data['name']}"
                )
                pass
            else:
                pantry_item = pantry_item_form.save(commit=False)
                pantry_item.user = request.user
                pantry_item.category = category
                pantry_item.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Added new item - {pantry_item_form.cleaned_data['name']}"
                )
            return redirect('pantry')
        return self.get(request, * args, **kwargs)
