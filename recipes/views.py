from django.shortcuts import render


def recipes_list(request):
    """
    Display a list of all recipes
    """
    context = {
        'page_title': 'Recipes',
    }
    return render(request, 'recipes/recipes_list.html', context)
