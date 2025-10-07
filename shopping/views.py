from datetime import date, datetime, time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from meals.models import MealPlanItem
from pantry.models import PantryItem
from pantry.pantry_search import PantrySearch
from .models import ShoppingList, ShoppingListItem
from .forms import ShoppingListForm


@login_required
def shopping_list(request, shopping_list_id=None):
    """
    Display shopping list page
    related to :model:`ShoppingList` and :model:`ShoppingListItem`

    ** Context **
        `list_this_week`: instance of :model:`ShoppingList` for
            current week
        `previous_lists` : instances of :model:`ShoppingList` except
            this week's
        `detail_for` : Dict with details for shopping list to display

    **Template:**
    :template:`shopping/shopping_list.html`
    """
    if request.method == "POST":
        shopping_list_form = ShoppingListForm(request.POST)
        if shopping_list_form.is_valid():
            cleaned_data = shopping_list_form.cleaned_data

            shopping_list, created = ShoppingList.objects.get_or_create(
                user=request.user,
                week_start_date=cleaned_data['week_start_date'],
                defaults={
                    'week_end_date': cleaned_data['week_end_date'],
                }
            )

            if created:
                generate_shopping_list_items(
                    request=request,
                    shopping_list_id=shopping_list.id,
                )
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    f"Created shopping list for "
                    f"{shopping_list_form.cleaned_data['week_start_date']}:"
                    f"{shopping_list_form.cleaned_data['week_end_date']}"
                )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Error generating shopping list"
            )
        return redirect(
            'shopping_detail',
            shopping_list_id=shopping_list.id
        )

    # get this week's list
    today = date.today()
    list_this_week = ShoppingList.objects.filter(
        user=request.user,
        week_start_date__lte=today,
        week_end_date__gte=today
    ).first()

    # find previous shopping lists
    shopping_lists = ShoppingList.objects.filter(
        user=request.user
    )
    previous_lists = (
        shopping_lists.exclude(id=list_this_week.id)
        if list_this_week else shopping_lists
    )

    # shopping list details based on id
    # By default this week's shopping list items
    if not shopping_list_id:
        shopping_list_id = list_this_week.id if list_this_week else None

    if shopping_list_id:
        shopping_list = shopping_lists.filter(id=shopping_list_id).first()

        planned_meals = get_planned_meals(
            request,
            shopping_list.week_start_date,
            shopping_list.week_end_date,
        )

        # Group planned meals by day of the week
        planned_meals_by_day = group_meals_by_day(planned_meals)

        # Filter shopping list items by in_pantry status
        items_to_buy = shopping_list.shopping_list_items.filter(
            in_pantry=False
        )
        items_in_pantry = shopping_list.shopping_list_items.filter(
            in_pantry=True
        )

        detail_for = {
            'shopping_list': shopping_list,
            'planned_meals_by_day': planned_meals_by_day,
            'items_to_buy': items_to_buy,
            'items_in_pantry': items_in_pantry,
        }
    else:
        detail_for = None

    context = {
        'page_title': 'Shopping Lists',
        'list_this_week': list_this_week,
        'previous_lists': previous_lists,
        'detail_for': detail_for,
    }
    return render(request, 'shopping/shopping_list.html', context)


@login_required
def delete_shopping_list(request, shopping_list_id):
    """
    Deletes an instance of shopping list
    related to :model:`ShoppingList`
    """
    shopping_list = get_object_or_404(
        ShoppingList.objects.filter(
            pk=shopping_list_id,
            user=request.user
        )
    )

    # User specified while fetching record
    # so proceed to delete
    shopping_list.delete()
    messages.add_message(
        request,
        messages.SUCCESS,
        f'Shopping list removed - '
        f'{shopping_list.week_start_date}:{shopping_list.week_end_date}'
    )
    return redirect('shopping')


@login_required
def generate_shopping_list_items(request, shopping_list_id):
    """
    Generate instances of :model:`ShoppingListItem` for
    :model:`ShoppingList` based on instances of
    :model:`MealPlanItem` available for the week
    """
    shopping_list = get_object_or_404(ShoppingList.objects.filter(
        user=request.user,
        pk=shopping_list_id,
    ))

    planned_meals = get_planned_meals(
        request,
        shopping_list.week_start_date,
        shopping_list.week_end_date,
    )

    pantry_items = PantryItem.objects.filter(
        user=request.user,
    )

    ingredients_to_shop = {}
    ingredients_in_pantry = {}
    for meal in planned_meals:
        meal_ingredients = meal.recipe.ingredients.all()
        matched, _, missing = PantrySearch().find_match(
            recipe_ingredients=meal_ingredients,
            pantry_items=pantry_items,
        )
        for ingredient in missing:
            if ingredient in ingredients_to_shop:
                ingredients_to_shop[ingredient]['recipe'].append(meal.recipe)
            else:
                ingredients_to_shop[ingredient] = {
                    'quantity': meal_ingredients.filter(
                        ingredient_name=ingredient
                    ).first().quantity,
                    'units': meal_ingredients.filter(
                        ingredient_name=ingredient
                    ).first().units,
                    'recipe': [meal.recipe],
                }

        for ingredient, pantry_item, _ in matched:
            if ingredient in ingredients_in_pantry:
                ingredients_in_pantry[ingredient]['recipe'].append(meal.recipe)
            else:
                ingredients_in_pantry[ingredient] = {
                    'quantity': meal_ingredients.filter(
                        ingredient_name=ingredient
                    ).first().quantity,
                    'units': meal_ingredients.filter(
                        ingredient_name=ingredient
                    ).first().units,
                    'recipe': [meal.recipe],
                    'pantry_item': pantry_item,
                }

    # Create ShoppingListItem objects for each ingredient to shop
    for ingredient_name, ingredient_data in ingredients_to_shop.items():
        # Create a new shopping list item
        try:
            ShoppingListItem.objects.create(
                shopping_list=shopping_list,
                item_name=ingredient_name,
                quantity=ingredient_data['quantity'],
                units=ingredient_data['units'],
                notes=(
                    "Needed for: " +
                    ", ".join(
                        [recipe.title for recipe in ingredient_data['recipe']]
                    )
                ),
                in_pantry=False,
            )
        except Exception as e:
            messages.add_message(
                request,
                messages.WARNING,
                f"Error adding ingredients to shopping list- {e}"
            )
            break

    # Create ShoppingListItems to keep track of items in pantry
    for ingredient_name, ingredient_data in ingredients_in_pantry.items():
        # Create a new shopping list item
        try:
            ShoppingListItem.objects.create(
                shopping_list=shopping_list,
                item_name=ingredient_name,
                quantity=ingredient_data['quantity'],
                units=ingredient_data['units'],
                notes=(
                    "Needed for: " +
                    ", ".join(
                        [recipe.title for recipe in ingredient_data['recipe']]
                    )
                ),
                in_pantry=True,
            )
        except Exception as e:
            messages.add_message(
                request,
                messages.WARNING,
                f"Error adding ingredients to shopping list- {e}"
            )
            break


@login_required
def refresh_shopping_list(request, shopping_list_id):
    """
    Refresh the :model:`ShoppingListItem`s related to
    :model:`ShoppingList`
    - Deletes existing items and regenerates new ones
    """
    shopping_list = get_object_or_404(ShoppingList.objects.filter(
        user=request.user,
        pk=shopping_list_id,
    ))

    # delete existing shopping list items
    for item in shopping_list.shopping_list_items.all():
        item.delete()

    # generate the shopping list items
    generate_shopping_list_items(request, shopping_list.id)

    return redirect(
        'shopping_detail',
        shopping_list_id=shopping_list.id
    )


@login_required
def get_planned_meals(request, week_start, week_end):
    """
    """
    # Convert dates to datetime objects for proper comparison
    week_start_datetime = timezone.make_aware(datetime.combine(
        week_start,
        time.min
    ))  # Start of day
    week_end_datetime = timezone.make_aware(datetime.combine(
        week_end,
        time.max
    ))  # End of day

    planned_meals = MealPlanItem.objects.filter(
        user=request.user,
        start_time__gte=week_start_datetime,
        start_time__lte=week_end_datetime,
    )

    return planned_meals


def group_meals_by_day(planned_meals):
    """
    Group planned meals by day of the week
    Args:
        planned_meals: QuerySet or list of MealPlanItem objects

    Returns:
        dict: {
            'Monday': [meal1, meal2, ...],
            'Tuesday': [meal3, meal4, ...],
            ...
        }
    """
    # Initialize dictionary with all days of the week
    days_of_week = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'
    ]
    meals_by_day = {}

    # Initialize all days with empty lists
    for day in days_of_week:
        meals_by_day[day] = []

    # Group meals by day
    for meal in planned_meals:
        day_name = meal.start_time.strftime('%A')
        meals_by_day[day_name].append(meal)

    return meals_by_day
