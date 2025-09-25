from django.shortcuts import render


def recipes_list(request):
    """
    Display a list of all recipes
    """
    context = {
        'page_title': 'My Recipes',
    }
    return render(request, 'recipes/recipes_list.html', context)
