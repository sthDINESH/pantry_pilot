from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from recipes.models import SavedRecipe


@login_required
def meals_list(request):
    """
    Display meals planning page with selected recipes
    """
    selected_recipe_ids = request.session.get('selected_for_meal_plan', [])
    selected_recipes = SavedRecipe.objects.filter(
        id__in=selected_recipe_ids,
        user=request.user
    )
    context = {
        'page_title': 'Meal Planning',
        'selected_recipes': selected_recipes,
        'selected_count': selected_recipes.count(),
    }
    return render(request, 'meals/meals_list.html', context)
