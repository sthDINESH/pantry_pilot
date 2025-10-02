from datetime import datetime, timedelta
from dateutil.parser import parse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from recipes.models import SavedRecipe
from .models import MealPlanItem


@login_required
def meal_planning(request):
    """
    Display meals planning page with list of selected recipes from session

    **Context:**
    `selected_recipes`:
        List of recipes selected by user and saved in Django's session
    `selected_count`:
        Count of selected recipes
    
    **Template:**
    :template:`meals/meal_planning.html`
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
    return render(request, 'meals/meal_planning.html', context)


@login_required
def get_meal_plan(request):
    """
    Generate and return a JSON response containing 
    a list of Full calendar event objects with details
    populated from meal plan items within `start` and `end`
    query string params

    Supports AJAX requests from events field within Full Calendar
    objects

    **Context**
    `meal_plan_item`

    **Template**
    :template:`meals/meals_list.html`
    """
    # Pick start and end datetimes from query strings
    start_date_str = request.GET.get("start")
    end_date_str = request.GET.get("end")

    if start_date_str and end_date_str:
        start_date = parse(start_date_str)
        end_date = parse(end_date_str)
    else:
        start_date = datetime.now()
        end_date = start_date + timedelta(days=7)

    meal_plan_items = MealPlanItem.objects.filter(
        user=request.user,
        start_time__range=(start_date, end_date)
    )

    # AJAX response
    return JsonResponse([
        {
            "id": item.id,
            "title": item.recipe.title if item.recipe else "Meal",
            "start": item.start_time.isoformat(),
            "end": None,  # Add item.end if you have an end datetime
            "allDay": False,
            "extendedProps": {
                "meal_type": item.meal_type,
                "servings": item.servings,
                "recipe_id": item.recipe.id if item.recipe else None,
            },
        } for item in meal_plan_items
    ], safe=False)
