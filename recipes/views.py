import time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from pantry.models import PantryItem
from pantry.pantry_search import PantrySearch
from .forms import RecipeSearchForm
from .models import SavedRecipe, RecipeIngredient
from .spoonacular import SpoonacularApiService


@login_required
def recipes_list(request):
    """
    Display a single recipe item
    - related to :model:`SavedRecipe`
    - and search results based on submitted :form:`RecipeSearchForm`
    ** Context: **
        `recipe_search_form`: instance of :form:`RecipeSearchForm`
        `search results`: object with search results
            'query_data': search query data
            'response': {}
            'timestamp': int
        `saved_recipes_json`: JSON derived from instances of
            :model:`SavedRecipe`
        `selected_for_meal_plan`: []
            (recipes selected for meal planning available in session)
    ** Template: **
    :template:`recipes/recipes_list.html`
    """
    # Fetch users pantry items
    pantry_items = PantryItem.objects.filter(user=request.user)
    pantry_item_names = [
        pantry_item.name
        for pantry_item in pantry_items
    ]

    # Post request for recipe searches
    # search params submitted via :forms:`RecipeSearchForm`
    if request.method == "POST":
        recipe_search_form = RecipeSearchForm(request.POST)
        if recipe_search_form.is_valid():
            search_data = recipe_search_form.cleaned_data

            # Search recipes using Spoonacular API
            search_results = SpoonacularApiService().search_recipes(
                ingredients=pantry_item_names,
                cuisine=search_data["cuisine"],
                diet=search_data["diet"],
                meal_type=search_data["meal_type"],
            )

            # Store search results in session
            request.session['recipe_search_state'] = {
                'query_data': search_data,
                'timestamp': int(time.time()),
                'response': search_results,
            }
            # Clear any previous recipe details from session
            request.session['recipe_detail_state'] = {}
            # Ensure session is saved
            request.session.modified = True

            return redirect('recipes')

    # Fetch saved recipes
    saved_recipes = SavedRecipe.objects.filter(
        user=request.user,
        is_external=True,
    )

    # Add ingredient analysis to each saved recipe
    saved_recipes_json = []
    for recipe in saved_recipes:
        ingredients = recipe.ingredients.all()

        matched_ingredients, similar_ingredients, missing_ingredients = (
            PantrySearch().find_match(
                recipe_ingredients=ingredients,
                pantry_items=pantry_items
            )
        )
        missing_ingredients = missing_ingredients
        similar_ingredients = similar_ingredients
        matched_ingredients = matched_ingredients

        saved_recipes_json.append(
            {
                'id': recipe.id,
                'title': recipe.title,
                'image': (
                    recipe.api_image_url
                    if recipe.is_external else recipe.image
                ),
                'matched_ingredients': [
                    recipe_ing.ingredient_name
                    for (recipe_ing, pantry_item, _)
                    in matched_ingredients
                ],
                'similar_ingredients': [
                    {recipe_ing.ingredient_name: pantry_item.name}
                    for (recipe_ing, pantry_item, _)
                    in similar_ingredients
                ],
                'missing_ingredients': [
                    recipe_ing.ingredient_name
                    for recipe_ing
                    in missing_ingredients
                ],
            }
        )

    # Check if search results persist in session
    if 'recipe_search_state' in request.session:
        search_results = request.session['recipe_search_state']
        form_data = search_results["query_data"]
        recipe_search_form = RecipeSearchForm(initial=form_data)

        # Check and mark recipes that have already been saved
        if search_results.get("response", {}).get("success"):
            saved_recipe_api_ids = {
                r.api_recipe_id for r in saved_recipes
            }
            for recipe in search_results['response']['recipes']:
                recipe['saved'] = (
                    recipe['api_recipe_id'] in saved_recipe_api_ids
                )
                # For already saved results add recipe id(PK)
                # for direct links to saved version
                if recipe['saved']:
                    saved_recipe = next(
                        (
                            r for r in saved_recipes
                            if r.api_recipe_id == recipe['api_recipe_id']
                        ),
                        None
                    )
                    recipe['id'] = saved_recipe.id if saved_recipe else None
                else:
                    recipe['id'] = None
    else:
        search_results = None
        recipe_search_form = RecipeSearchForm()

    # Get selected recipes for meal planning from session
    selected_for_meal_plan = request.session.get('selected_for_meal_plan', [])

    context = {
        'recipe_search_form': recipe_search_form,
        'search_results': search_results,
        'saved_recipes_json': saved_recipes_json,
        'selected_for_meal_plan': selected_for_meal_plan,
    }
    return render(request, 'recipes/recipes_list.html', context)


@login_required
def toggle_recipe_selection(request, recipe_id):
    """
    Add or remove a recipe from the user's meal planning selection
    (session-based). Supports AJAX requests.
    """
    selected_recipes = request.session.get('selected_for_meal_plan', [])
    recipe_id_str = str(recipe_id)

    toggled = False
    if recipe_id_str in selected_recipes:
        selected_recipes.remove(recipe_id_str)
        toggled = False
    else:
        selected_recipes.append(recipe_id_str)
        toggled = True

    request.session['selected_for_meal_plan'] = selected_recipes
    request.session.modified = True

    # AJAX response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'selected': toggled,
            'selected_for_meal_plan': selected_recipes,
            'message': "Added" if toggled else "Removed"
        })

    # Non-AJAX fallback (redirect)
    if toggled:
        messages.success(request, "Recipe added to meal planning selection.")
    else:
        messages.info(request, "Recipe removed from meal planning selection.")

    from_tab = request.GET.get('from', '')
    if from_tab in ['saved', 'my-recipes']:
        recipes_url = reverse('recipes')
        return HttpResponseRedirect(f'{recipes_url}?tab={from_tab}')
    else:
        return redirect('recipes')


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

    # Handle from 'query' parameter if present
    from_tab = request.GET.get('from')

    if from_tab in ['discover']:
        return redirect('recipes')
    else:
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
