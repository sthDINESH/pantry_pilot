from datetime import date, datetime, time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from meals.models import MealPlanItem
from .models import ShoppingList


@login_required
def shopping_list(request, shopping_list_id=None):
    """
    Display shopping list page with basic message
    
    **Template:**
    :template:`shopping/shopping_list.html`
    """
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

        # Convert dates to datetime objects for proper comparison
        week_start_datetime = timezone.make_aware(datetime.combine(
            shopping_list.week_start_date,
            time.min
        ))  # Start of day
        week_end_datetime = timezone.make_aware(datetime.combine(
            shopping_list.week_end_date,
            time.max
        ))  # End of day

        planned_meals = MealPlanItem.objects.filter(
            user=request.user,
            start_time__gte=week_start_datetime,
            start_time__lte=week_end_datetime,
        )
        detail_for = {
            'shopping_list': shopping_list,
            'planned_meals': planned_meals,
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
