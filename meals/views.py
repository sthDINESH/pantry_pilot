from datetime import datetime, timedelta
from dateutil.parser import parse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from recipes.models import SavedRecipe
from .models import MealPlanItem
from .forms import MealPlanItemForm


@login_required
def meal_planning(request):
    """
    Display meals planning page with list of selected recipes from session

    **Context:**
    `selected_recipes`:
        List of recipes selected by user and saved in Django's session
    `selected_count`:
        Count of selected recipes
    `meal_plan_item_form`:
        Instance of :form:`MealPlanItemForm`

    **Template:**
    :template:`meals/meal_planning.html`
    """
    if request.method == "POST":
        # Form submission is through an AJAX request
        # Sends JSON response with success to frontend JS
        meal_plan_item_form = MealPlanItemForm(request.POST)

        if meal_plan_item_form.is_valid():
            meal_plan_item = meal_plan_item_form.save(commit=False)
            meal_plan_item.user = request.user
            meal_plan_item.save()

            return JsonResponse({
                'success': True,
                'message': f"Added {meal_plan_item.recipe.title} to meal plan",
            })
        else:
            print("Form data has errors")
            print(meal_plan_item_form.errors)
            return JsonResponse({
                'success': False,
                'error': meal_plan_item_form.errors,
                'message': "Error saving recipe to meal plans",
            })

    selected_recipe_ids = request.session.get('selected_for_meal_plan', [])
    selected_recipes = SavedRecipe.objects.filter(
        id__in=selected_recipe_ids,
        user=request.user
    )

    meal_plan_item_form = MealPlanItemForm()

    context = {
        'selected_recipes': selected_recipes,
        'selected_count': selected_recipes.count(),
        'meal_plan_item_form': meal_plan_item_form,
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
            "end": item.end_time.isoformat(),
            "allDay": False,
            "classNames": f"meal-type-{item.meal_type}",
            "textColor": "black",
            "borderColor": "white",
            "extendedProps": {
                "meal_type": item.meal_type,
                "servings": item.servings,
                "recipe_id": item.recipe.id if item.recipe else None,
            },
        } for item in meal_plan_items
    ], safe=False)


@login_required
def delete_meal_plan_item(request, meal_plan_item_id):
    """
    Delete a meal plan item related to :model:`MealPlanItem`
    Supports AJAX POST request from `eventClick` callbacks from FullCalender
    Returns a JSON response with status
    """
    try:

        meal_plan_item = MealPlanItem.objects.get(
            pk=meal_plan_item_id,
            user=request.user,
        )

        # User specified while fetching record
        # so proceed to delete
        meal_plan_item.delete()
        return JsonResponse({
            'success': True,
            'message': f'{meal_plan_item.recipe.title} removed from plan.'
        })
    except MealPlanItem.DoesNotExist:
        return JsonResponse(
            {
                'success': False,
                'message': 'Meal plan item not found.'
            },
            status=404
        )
    except Exception as e:
        # Handle other exceptions
        return JsonResponse(
            {
                'success': False,
                'message': f'Error: {str(e)}'
            },
            status=500
        )


@login_required
def update_meal_plan_item(request, meal_plan_item_id):
    """
    Update meal plan item related to :model:`MealPlanItem`
    Supports AJAX POST request from `eventClick` callbacks from FullCalender
    Returns a JSON response with status
    """
    if request.method == "POST":
        try:
            meal_plan_item = MealPlanItem.objects.get(
                pk=meal_plan_item_id,
                user=request.user,
            )

            meal_plan_item_form = MealPlanItemForm(
                data=request.POST,
                instance=meal_plan_item
            )

            if meal_plan_item_form.is_valid():
                # User specified while fetching record
                # so proceed to save
                meal_plan_item_form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Meal plan updated.'
                })
            else:
                return JsonResponse(
                    {
                        'success': False,
                        'message': (
                            'Not updated - Errors in submitted meal plan item'
                        )
                    }
                )
        except MealPlanItem.DoesNotExist:
            return JsonResponse(
                {
                    'success': False,
                    'message': 'Meal plan item not found.'
                },
                status=404
            )
        except Exception as e:
            # Handle other exceptions
            return JsonResponse(
                {
                    'success': False,
                    'message': f'Error: {str(e)}'
                },
                status=500
            )
    else:
        return JsonResponse(
                {
                    'success': False,
                    'message': 'Unsupported request.'
                },
                status=405
            )
