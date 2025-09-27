from django.shortcuts import render, redirect

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

            # Store search results in session for retrieval after redirect
            request.session['search_results'] = {
                'query_data': search_data,
                'message': (
                    f"Searching for {search_data['cuisine'] or 'any cuisine'} "
                    f"{search_data['diet'] or 'any diet'} "
                    f"{search_data['meal_type'] or 'any meal type'} recipes"
                )
            }

            # Fetch users pantry items
            ingredient_names = [
                pantry_item.name
                for pantry_item in PantryItem.objects.filter(user=request.user)
            ]
            # request.session['search_results']['ingredients'] = ingredients

            # Search recipes based on pantry items and search query
            search_results = SpoonacularApiService().search_recipes(
                ingredients=ingredient_names,
                cuisine=search_data["cuisine"],
                diet=search_data["diet"],
                meal_type=search_data["meal_type"],
            )
            request.session['search_results']['response'] = search_results

            return redirect('recipes')

    # Check for search results from session (after redirect)
    if 'search_results' in request.session:
        search_results = request.session.pop('search_results')
        form_data = search_results["query_data"]
        recipe_search_form = RecipeSearchForm(initial=form_data)

    context = {
        'recipe_search_form': recipe_search_form,
        'search_results': search_results,
    }
    return render(request, 'recipes/recipes_list.html', context)

