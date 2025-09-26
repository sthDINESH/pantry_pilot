from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import RecipeSearchForm


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

            # Store form data to repopulate form
            request.session['search_form_data'] = search_data

            # TODO: Add Spoonacular API results to session
            # api_results = call_spoonacular_api(search_data)
            # request.session['search_results']['api_data'] = api_results

            return redirect('recipes')

    # Check for search results from session (after redirect)
    if 'search_results' in request.session:
        search_results = request.session.pop('search_results')

    # Repopulate form with previous search data if available
    if 'search_form_data' in request.session:
        form_data = request.session.pop('search_form_data')
        recipe_search_form = RecipeSearchForm(initial=form_data)

    context = {
        'page_title': 'Recipes',
        'recipe_search_form': recipe_search_form,
        'search_results': search_results,
    }
    return render(request, 'recipes/recipes_list.html', context)

