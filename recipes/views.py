from django.shortcuts import render, redirect
import time

from .forms import RecipeSearchForm
from .spoonacular import SpoonacularApiService
from pantry.models import PantryItem


def recipes_list(request):
    """
    Display recipes list and handle search functionality
    """
    recipe_search_form = RecipeSearchForm()
    search_results = None

    if request.method == "POST":
        recipe_search_form = RecipeSearchForm(request.POST)
        if recipe_search_form.is_valid():
            search_data = recipe_search_form.cleaned_data

            # Store search results persistently in session
            request.session['recipe_search_state'] = {
                'query_data': search_data,
                'message': (
                    f"Searching for {search_data['cuisine'] or 'any cuisine'} "
                    f"{search_data['diet'] or 'any diet'} "
                    f"{search_data['meal_type'] or 'any meal type'} recipes"
                ),
                'timestamp': int(time.time())  # For cache expiry if needed
            }

            # Fetch users pantry items
            ingredient_names = [
                pantry_item.name
                for pantry_item in PantryItem.objects.filter(user=request.user)
            ]

            # Search recipes
            search_results = SpoonacularApiService().search_recipes(
                ingredients=ingredient_names,
                cuisine=search_data["cuisine"],
                diet=search_data["diet"],
                meal_type=search_data["meal_type"],
            )

            # Store search results persistently
            request.session['recipe_search_state']['response'] = search_results
            request.session.modified = True  # Ensure session is saved

            return redirect('recipes')

    # ✅ Check for persistent search results (don't pop)
    if 'recipe_search_state' in request.session:
        search_results = request.session['recipe_search_state']
        form_data = search_results["query_data"]
        recipe_search_form = RecipeSearchForm(initial=form_data)

    context = {
        'recipe_search_form': recipe_search_form,
        'search_results': search_results,
    }
    return render(request, 'recipes/recipes_list.html', context)


def recipe_detail(request, recipe_id):
    """
    Display recipe details
    """
    recipe_detail = SpoonacularApiService().get_recipe_details(
        recipe_id=recipe_id,
        user_id=request.user.id
    )
    print(recipe_detail)

    return render(
        request=request,
        template_name="recipes/recipe_detail.html",
        context={
            'recipe_id': recipe_id,
            'recipe_detail': recipe_detail,
        }
    )

