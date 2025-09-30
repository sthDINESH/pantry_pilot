import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RecipeSearchForm
from pantry.models import PantryItem
from .models import SavedRecipe, RecipeIngredient
from .spoonacular import SpoonacularApiService


@login_required
def recipes_list(request):
    """
    Display recipes list and handle search functionality
    """
    recipe_search_form = RecipeSearchForm()
    search_results = None

    # Fetch users pantry items
    pantry_item_names = [
        pantry_item.name
        for pantry_item in PantryItem.objects.filter(user=request.user)
    ]
    print(pantry_item_names)

    # Fetch saved recipes with ingredient analysis
    saved_recipes = SavedRecipe.objects.filter(
        user=request.user,
        is_external=True,
    )

    # Add ingredient analysis to each recipe
    saved_recipes_with_notes = []
    for recipe in saved_recipes:
        ingredients = recipe.ingredients.all()
        missed_ingredients = []
        used_ingredients = []

        for ingredient in ingredients:
            if ingredient.ingredient_name in pantry_item_names:
                used_ingredients.append(ingredient)
                print("Found:", ingredient.ingredient_name)
            else:
                missed_ingredients.append(ingredient)
                print("Missing:", ingredient.ingredient_name)

        # Add notes directly to recipe object
        recipe.missed_ingredients = missed_ingredients
        recipe.used_ingredients = used_ingredients
        recipe.missed_ingredient_count = len(missed_ingredients)
        recipe.used_ingredient_count = len(used_ingredients)

        saved_recipes_with_notes.append(recipe)

    if request.method == "POST":
        recipe_search_form = RecipeSearchForm(request.POST)
        if recipe_search_form.is_valid():
            search_data = recipe_search_form.cleaned_data

            # Store search results persistently in session
            request.session['recipe_search_state'] = {
                'query_data': search_data,
                'message': (
                    f"Searching for {search_data['cuisine'] or 'any cuisine'} "
                    f"{search_data['diet'] or 'any diet'} "
                    f"{search_data['meal_type'] or 'any meal type'} recipes"
                ),
                'timestamp': int(time.time())
            }

            # Search recipes
            search_results = SpoonacularApiService().search_recipes(
                ingredients=pantry_item_names,
                cuisine=search_data["cuisine"],
                diet=search_data["diet"],
                meal_type=search_data["meal_type"],
            )

            # Store search results persistently
            request.session['recipe_search_state']['response'] = search_results
            request.session.modified = True  # Ensure session is saved

            return redirect('recipes')

    # Check for persistent search results (don't pop)
    if 'recipe_search_state' in request.session:
        search_results = request.session['recipe_search_state']
        form_data = search_results["query_data"]
        recipe_search_form = RecipeSearchForm(initial=form_data)

    context = {
        'recipe_search_form': recipe_search_form,
        'search_results': search_results,
        'saved_recipes': saved_recipes_with_notes,
        'number_saved_recipes': len(saved_recipes_with_notes),
    }
    return render(request, 'recipes/recipes_list.html', context)


@login_required
def recipe_detail(request, api_recipe_id):
    """
    Display recipe details
    """
    recipe_detail = fetch_recipe_detail(request, api_recipe_id)

    return render(
        request=request,
        template_name="recipes/recipe_detail.html",
        context={
            'recipe_detail': recipe_detail,
        }
    )


@login_required
def saved_recipe_detail(request, recipe_id):
    """
    Fetch saved recipe related to :model:`SavedRecipe` with pk=recipe_id
    and render using recipe_detail.html template
    """
    queryset = SavedRecipe.objects.filter(
        user=request.user,
    )
    saved_recipe = get_object_or_404(queryset, id=recipe_id)

    recipe_detail = {}
    recipe_detail['success'] = True
    recipe_detail['recipe'] = saved_recipe

    return render(
        request=request,
        template_name="recipes/recipe_detail.html",
        context={
            'recipe_detail': recipe_detail,
            'saved_recipe': True,
        }
    )


@login_required
def recipe_save(request, api_recipe_id):
    """
    Save recipe details for recipe_id for the user
    """
    recipe_detail = fetch_recipe_detail(request, api_recipe_id)

    saved_recipe, created = SavedRecipe.objects.get_or_create(
        user=request.user,
        api_recipe_id=api_recipe_id,
        defaults={
            # All other fields go in defaults
            'api_image_url': recipe_detail['recipe']['api_image_url'],
            'api_source_url': recipe_detail['recipe']['api_source_url'],
            'is_external': True,
            'title': recipe_detail['recipe']['title'],
            'summary': recipe_detail['recipe']['summary'],
            'cook_time': recipe_detail['recipe']['cook_time'],
            'cook_time_units': "min",
            'servings': recipe_detail['recipe']['servings'],
            'instructions': recipe_detail['recipe']['instructions'],
            'status': 1,
        }
    )

    # Save ingredients for the recipe
    if created:
        for ingredient in recipe_detail['recipe']['ingredients']:
            RecipeIngredient.objects.create(
                recipe=saved_recipe,
                ingredient_name=ingredient['name'],
                original_name=ingredient['original_name'],
                quantity=ingredient['amount'],
                units=ingredient['unit'],
                note=ingredient['note'],
                metric_quantity=ingredient['metric']['amount'],
                metric_units=ingredient['metric']['unitShort'],
            )

        messages.add_message(
            request,
            messages.SUCCESS,
            (
                f"Recipe saved - {saved_recipe.title}"
            )
        )

    else:
        messages.add_message(
            request,
            messages.WARNING,
            (
                f"Already saved - {saved_recipe.title}"
            )
        )

    return redirect('saved_recipe_detail', recipe_id=saved_recipe.id)


@login_required
def recipe_delete(request, recipe_id):
    """
    """
    queryset = SavedRecipe.objects.filter(user=request.user)
    saved_recipe = get_object_or_404(queryset, pk=recipe_id)

    if saved_recipe.user == request.user:
        saved_recipe.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            f'Recipe removed - {saved_recipe.title}'
        )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'You can only remove your recipes',
        )
    return redirect('recipes')


def fetch_recipe_detail(request, api_recipe_id):
    """
    """
    session_key = str(api_recipe_id)
    recipe_detail = None

    if 'recipe_detail_state' not in request.session:
        request.session['recipe_detail_state'] = {}

    # Check if recipe detail is available in session
    if (session_key in request.session['recipe_detail_state']):
        # Check if recipe detail is available in session
        # Fetch recipe detail from session
        recipe_detail = (
            request.session['recipe_detail_state'][session_key][
                'recipe_detail'
            ]
        )
        print("Fetched from session")
    else:
        # Make an API call
        recipe_detail = SpoonacularApiService().get_recipe_details(
            recipe_id=api_recipe_id,
            user_id=request.user.id
        )

        # Save recipe detail into session
        if recipe_detail['success']:
            request.session['recipe_detail_state'][session_key] = {
                'recipe_detail': recipe_detail,
                'timestamp': int(time.time()),
            }
            request.session.modified = True  # Ensure session is saved

    return recipe_detail
