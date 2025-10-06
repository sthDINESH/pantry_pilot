from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Category, PantryItem
from .forms import PantryItemForm, CategoryForm, ResolveDuplicateItemForm

# Create your views here.


def get_category_instance(request, name):
    # Get or create a category for the user depending on
    # whether the category already exists
    category, category_created = Category.objects.get_or_create(
        user=request.user,
        category_name=name,
    )
    if category_created:
        messages.add_message(
            request,
            messages.SUCCESS,
            (
                f"Added new category - "
                f"{category.get_category_name_display()}"
            )
        )
    return category


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
        category_form = CategoryForm(data=request.POST)
        pantry_item_form = PantryItemForm(data=request.POST)

        if category_form.is_valid() and pantry_item_form.is_valid():
            category = get_category_instance(
                self.request,
                category_form.cleaned_data['category_name']
            )

            # Check if pantry item already exists - needs resolution from user
            item_name = pantry_item_form.cleaned_data['name']
            existing_item = PantryItem.objects.filter(
                user=request.user,
                name=item_name,
            ).first()

            if existing_item:
                context = {
                    'categories': self.get_queryset(),
                    'pantry_item_form': PantryItemForm(),
                    'category_form': CategoryForm(),
                    # Render the template with resolution modal displayed
                    'show_duplicate_modal': True,
                    'existing_item': existing_item,
                    'form_data': {
                        'quantity': (
                            pantry_item_form.cleaned_data['quantity']
                        ),
                        'units_display': (
                            dict(PantryItem.UNIT_CHOICES)[
                                pantry_item_form.cleaned_data['units']
                            ]
                        ),
                        'category': category.category_name,
                        'category_display': (
                            category.get_category_name_display()
                        ),
                    },
                }
                # Add relevant forms to context for user feedback
                # These pre-populated forms are passed back to
                # resolve_duplicate_pantry_item view based on user selection
                if (
                    existing_item.units
                    == pantry_item_form.cleaned_data['units']
                ):
                    context["add_quantity_form"] = ResolveDuplicateItemForm(
                        initial={
                            'action': 'add_quantity',
                            'quantity':
                                pantry_item_form.cleaned_data['quantity'],
                        }
                    )
                context["replace_quantity_form"] = ResolveDuplicateItemForm(
                    initial={
                        'action': 'replace_quantity',
                        'quantity': pantry_item_form.cleaned_data['quantity'],
                        'units': pantry_item_form.cleaned_data['units'],
                        'category': category.category_name,
                    }
                )
                context["cancel_form"] = ResolveDuplicateItemForm(
                    initial={
                        'action': 'cancel',
                    }
                )
                return render(
                    request=request,
                    context=context,
                    template_name=self.template_name,
                )
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
        else:
            messages.add_message(
                request,
                messages.ERROR,
                (
                    f"Error adding item - {request.POST['name']}"
                )
            )
        return self.get(request, * args, **kwargs)


@login_required
def delete_pantry_item(request, item_id):
    """
    View to delete pantry item objects
    """
    queryset = PantryItem.objects.filter(user=request.user)
    pantry_item = get_object_or_404(queryset, pk=item_id)

    if pantry_item.user == request.user:
        pantry_item.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            f'Item removed - {pantry_item.name}'
        )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'You can only remove your items',
        )
    return redirect('pantry')


@login_required
def update_pantry_item(request, item_id):
    """
    View to update existing pantry item objects
    """
    if request.method == "POST":
        pantry_item = get_object_or_404(PantryItem, pk=item_id)

        pantry_item_form = PantryItemForm(
            data=request.POST,
            instance=pantry_item
        )
        category_form = CategoryForm(data=request.POST)

        if category_form.is_valid() and pantry_item_form.is_valid():
            category = get_category_instance(
                request, category_form.cleaned_data['category_name']
            )
            if pantry_item.user == request.user:
                pantry_item = pantry_item_form.save(commit=False)
                pantry_item.category = category
                pantry_item.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Updated item - {pantry_item_form.cleaned_data['name']}"
                )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    (
                        f"Error updating item - "
                        f"{pantry_item_form.cleaned_data['name']}."
                        " You can only update your items."
                    )
                )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                (
                    f"Error updating item - "
                    f"{pantry_item_form.cleaned_data['name']}."
                )
            )
        return redirect('pantry')


@login_required
def resolve_duplicate_pantry_item(request, item_id):
    """
    View to add to existing pantry item quantity when duplicate is detected
    """
    if request.method == "POST":
        resolution = ResolveDuplicateItemForm(request.POST)
        if resolution.is_valid():
            pantry_item = get_object_or_404(
                PantryItem,
                pk=item_id,
                user=request.user
            )
            action = resolution.cleaned_data["action"]
            if action == "add_quantity":
                # Add to existing quantity
                additional_quantity = resolution.cleaned_data["quantity"]
                pantry_item.quantity += additional_quantity
                pantry_item.save()

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    (
                        (
                            f"Updated {pantry_item.name} - added "
                            (
                                f"{additional_quantity} "
                                f"{pantry_item.get_units_display()}"
                            )
                        )
                    )
                )
            elif action == 'replace_quantity':
                # Replace existing quantity
                old_quantity = pantry_item.quantity
                pantry_item.quantity = resolution.cleaned_data['quantity']
                pantry_item.units = resolution.cleaned_data['units']
                category = get_category_instance(
                    request,
                    resolution.cleaned_data['category']
                )
                pantry_item.category = category
                pantry_item.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    (
                        f"Updated {pantry_item.name}"
                        f"- changed from {old_quantity} "
                        f"to {pantry_item.quantity} "
                        f"{pantry_item.get_units_display()}"
                    )
                )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                f"Error resolving duplicates for {pantry_item.name}"
            )
    return redirect('pantry')


@login_required
def delete_category(request, category_id):
    """
    View to delete categories from pantry
    """
    queryset = Category.objects.filter(user=request.user)
    category = get_object_or_404(queryset, pk=category_id)

    if category.user == request.user:
        category.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            f'Category removed - {category}'
        )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'You can only remove your categories',
        )
    return redirect('pantry')
