from django.shortcuts import render

from .forms import RecipeSearchForm


def recipes_list(request):
    """
    Display a list of all recipes
    """
    recipe_search_form = RecipeSearchForm()

    context = {
        'page_title': 'Recipes',
        'recipe_search_form': recipe_search_form,
    }
    return render(request, 'recipes/recipes_list.html', context)
