# Pantry Pilot - Testing

## Validation Testing

### HTML Validation
**[W3C Markup Validation Service](https://validator.w3.org/)** was used to validate the HTML on all pages of the site.
HTML was checked by running the validator with deployed page urls.

<details>
    <summary>Expand to view the results</summary>

| Page | Result | Evidence |
|------|--------|----------|
| Home Page (Dashboard) - Unauthenticated | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/dashboard_unauthenticated_page.png) |
| Home Page (Dashboard) - Authenticated | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/dashboard_unauthenticated_page.png) |
| Sign Up Page | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/signup_page.png) |
| Sign In Page | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/signin_page.png) |
| Sign Out Page | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/signout_page.png)<sup>1</sup> |
| Pantry Management | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/pantry_page_uri.png)<sup>2</sup>|
| Pantry Management | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/pantry_page_source.png)<sup>2</sup>|
| Recipe Discovery | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/recipes_page_uri.png)<sup>2</sup>|
| Recipe Discovery | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/recipes_page_source.png)<sup>2</sup>|
| Recipe Detail | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/recipe_detail_uri.png)<sup>2</sup>|
| Recipe Detail | ✅ Pass | [No errors or warnings](documentation/testing/html_validation/recipe_detail_source.png)<sup>2</sup>|
| Meal Planning | ✅ Pass | No errors or warnings found in HTML validation |
| Shopping Lists | ✅ Pass | No errors or warnings found in HTML validation |

Note:
- <sup>1</sup> Validation by deployed webpage's source code instead of URL because the validator kept redirecting to home page for the url. 
- <sup>2</sup> Validation by URI displays info about trailing slash on void elements, but when direct source is used for validation the warning is not seen.

</details>


### CSS Validation
**[W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)** was used to validate the custom CSS file for the site.
CSS was validated by running the validator with direct CSS source input.

<details>
    <summary>Expand to view the results</summary>

</details>


### Javascript Validation
**[JS Hint](https://jshint.com/)** was used to validate the custom Javascript file for the site.

<details>
    <summary>Expand to view the results</summary>
</details>


### Python Validation

**[Code Institute Python Linter](https://pep8ci.herokuapp.com/)** was used to validate the custom python files.
Flake8 extension for vsCode from Mircosoft was used during the development to help conform to PEP8 guidelines.

<details>
    <summary>Expand to view the results</summary>

| App Name | File | Result | Evidence |
|----------|------|--------|----------|
| **dashboard** | `dashboard/views.py` | ✅ Pass | [no errors or warnings](documentation/testing/python_validation/dashboard_views_py.png) |
| **dashboard** | `dashboard/forms.py` | ✅ Pass | [no errors or warnings](documentation/testing/python_validation/dashboard_forms_py.png) |
| **dashboard** | `dashboard/urls.py` | ✅ Pass | [no errors or warnings](documentation/testing/python_validation/dashboard_urls_py.png) |
| **pantry** | `pantry/apps.py` | ✅ Pass | Standard Django app configuration file |
| **pantry** | `pantry/models.py` | ✅ Pass | `PantryItem` and `Category` models with UNIT_CHOICES validation |
| **pantry** | `pantry/views.py` | ✅ Pass | CRUD operations for pantry items including `resolve_duplicate_pantry_item` |
| **pantry** | `pantry/forms.py` | ✅ Pass | `PantryItemForm` with manual floating labels and validation methods |
| **pantry** | `pantry/admin.py` | ✅ Pass | Admin registration for `PantryItemAdmin` and `CategoryAdmin` |
| **pantry** | `pantry/urls.py` | ✅ Pass | URL patterns for pantry CRUD operations and duplicate resolution |
| **recipes** | `recipes/apps.py` | ✅ Pass | Standard Django app configuration file |
| **recipes** | `recipes/models.py` | ✅ Pass | `SavedRecipe` and `RecipeIngredient` models with external API integration |
| **recipes** | `recipes/views.py` | ✅ Pass | Recipe search, save, and detail views with `SpoonacularApiService` integration |
| **recipes** | `recipes/forms.py` | ✅ Pass | `RecipeSearchForm` with manual floating labels to avoid HTML validation errors |
| **recipes** | `recipes/urls.py` | ✅ Pass | URL patterns for recipe operations including save and toggle selection |
| **recipes** | `recipes/spoonacular.py` | ✅ Pass | External API service class for recipe search and details |
| **meals** | `meals/apps.py` | ✅ Pass | Standard Django app configuration file |
| **meals** | `meals/models.py` | ✅ Pass | `MealPlanItem` model for meal planning functionality |
| **meals** | `meals/views.py` | ✅ Pass | Meal planning views including `meal_planning` and calendar operations |
| **meals** | `meals/forms.py` | ✅ Pass | `MealPlanItemForm` for adding meals to calendar |
| **meals** | `meals/admin.py` | ✅ Pass | Admin registration for `MealPlanItemAdmin` |
| **meals** | `meals/urls.py` | ✅ Pass | URL patterns for meal planning CRUD operations |
| **shopping** | `shopping/apps.py` | ✅ Pass | Standard Django app configuration file |
| **shopping** | `shopping/models.py` | ✅ Pass | `ShoppingList` and `ShoppingListItem` models |
| **shopping** | `shopping/views.py` | ✅ Pass | Shopping list generation with `generate_shopping_list_items` function |
| **shopping** | `shopping/forms.py` | ✅ Pass | `ShoppingListForm` for creating shopping lists |
| **shopping** | `shopping/urls.py` | ✅ Pass | URL patterns for shopping list operations |


</details>


