# Pantry Pilot - Testing

[Go back to Readme](README.md)

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
| **pantry** | `pantry/models.py` | ✅ Pass | [no errors or warnings](documentation/testing/python_validation/pantry_models_py.png) |
| **pantry** | `pantry/views.py` | ✅ Pass | [no errors or warnings](documentation/testing/python_validation/pantry_views_py.png)|
| **pantry** | `pantry/forms.py` | ✅ Pass | [no errors or warnings](documentation/testing/python_validation/pantry_forms_py.png) |
| **pantry** | `pantry/admin.py` | ✅ Pass | [no errors or warnings](documentation/testing/python_validation/pantry_admin_py.png) |
| **pantry** | `pantry/urls.py` | ✅ Pass | [no errors or warnings](documentation/testing/python_validation/pantry_urls_py.png) |
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

### Lighthouse Testing

Google Lighthouse was used to test performance, accessibility, best practices and SEO for the site.

<details>
    <summary>Expand to view the results</summary>
</details>

### Manual Testing

#### Testing User Stories

<details>
    <summary>Expand to view the results</summary>

<table>
  <thead>
    <tr>
      <th>ID</th>
      <th>User Story</th>
      <th>Testing</th>
      <th>Comments</th>
      <th>Results</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <td><strong>US001</strong></td>
        <td>
            <strong>AS A</strong> new user <strong>I WANT TO</strong> create an account with email and password <strong>SO THAT I CAN</strong> save my pantry data and access personalized features
        </td>
        <td>
            <ul>
                <li>Click on the SignUp link accessible through the navbar</li>
                <li>Fill in the username, email and password fields</li>
                <li>Click the Start button to register</li>
            </ul>
        </td>
        <td>
            <ul>
                <li>✅ User can access registration page from the navbar</li>
                <li>✅ Registration form includes username, email, password, and confirm password fields</li>
                <li>✅ Users can't submit empty form</li>
                <li>✅ Email field validates proper email format</li>
                <li>✅ Uniqueness for username checked</li>
                <li>✅ Password requirements are checked</li>
                <li>✅ Matching password and confirm password field checked</li>
                <li>✅ success message displayed upon successful registration</li>
                <li>✅ User is automatically logged in after registration</li>
                <li>✅ User redirected to dashboard after successful registration</li>
                <li>✅ Error messages display for invalid inputs</li>
                <li>✅ Duplicate email addresses are prevented with clear error message</li>
            </ul>
        </td>
        <td> Pass </td>
    </tr>
    <tr>
        <td><strong>US002</strong></td>
        <td><strong>AS A</strong> returning user <strong>I WANT TO</strong> log into my account <strong>SO THAT I CAN</strong> access my personal pantry</td>
        <td>
            <ul>
                <li>Click on the Login link in navbar</li>
                <li>Fill in the username and password, and click the button</li>
            </ul>
        </td>
        <td>
            <ul>
                <li>✅ Login form accessible from navigation</li>
                <li>✅ Login form accepts username and password</li>
                <li>✅ Username displayed in navbar after login</li>
                <li>✅ User redirected to dashboard after successful login</li>
                <li>✅ Error message displayed for invalid credentials</li>
                <li>✅ User stays on login page if credentials are invalid</li>
                <li>✅ Users can login without email verification</li>
            </ul>
        </td>
        <td> Pass </td>
    </tr>
    <tr>
        <td><strong>US003</strong></td>
        <td><strong>AS A</strong> logged in user <strong>I WANT TO</strong> log out of my account <strong>SO THAT I CAN</strong> secure my data when finished</td>
        <td>
            <ul>
                <li>When logged in, click on logout link accessible from dropdown link under username in navigation</li>
                <li>Click on the Sign Out button to confirm</li>
            </ul>
        </td>
        <td>
            <ul>
            <li>✅ Logout accessible from navigation for authenticated users</li>
            <li>✅ Clicking logout confirmation ends user session</li>
            <li>✅ User redirected to landing page after logout</li>
            <li>✅ Navigation bar changes to indicate logout state</li>
            <li>✅ Success message confirms successful logout</li>
            <li>✅ User cannot access protected pages after logout without re-authenticating</li>
            <li>✅ Logout works consistently across all pages</li>
            <li>✅ Logout link only appears for authenticated users</li>
            </ul>
        </td>
        <td> Pass </td>
    </tr>
    <tr>
        <td><strong>US004</strong></td>
        <td><strong>AS A</strong> logged in user <strong>I WANT TO</strong> add ingredients to my pantry with name and quantity <strong>SO THAT I CAN</strong> track what I have available</td>
        <td>
            <ul>
                <li>Access Pantry page from navigation</li> 
                <li>Fill in form with required name, quantity, units and category</li> 
                <li>Upload item image(optional)</li>
                <li>Click Add</li> 
            </ul>
        </td>
        <td>
            <ul>
                <li>✅ Form is accessible from pantry page</li>
                <li>✅ Form includes fields for name, quantity, unit, category and image</li>
                <li>✅ Item, quantity, units and category inputs are mandatory</li>
                <li>✅ Quantity entered must be a positive</li>
                <li>✅ Confirmation message displayed after successful addition</li>
                <li>✅ New item appears in pantry list immediately after addition</li>
                <li>✅ Form validates all required fields before submission</li>
                <li>✅ Checks if item already exits - users can add to or replace existing quantity if units match</li>
                <li>✅ Checks if item already exits - users can replace existing quantity if units don't match</li>
            </ul>
        </td>
        <td> Pass </td>
    </tr>
    <tr>
        <td><strong>US005</strong></td>
        <td><strong>AS A</strong> logged in user <strong>I WANT TO</strong> see all my pantry items in a list <strong>SO THAT I CAN</strong> quickly review what ingredients I have</td>
        <td>
            <ul>
                <li>Access Pantry page from navigation</li>
            </ul>
        </td>
        <td>
        <ul>
            <li>✅ Pantry page displays all user's items</li>
            <li>✅ Each item shows name, quantity, unit</li>
            <li>✅ Items are sectioned by category</li>
            <li>✅ Page displays item count per category</li>
            <li>✅ Message displayed for empty pantry</li>
            <li>✅ Add new item button is prominently displayed</li>
            <li>✅ User data is isolated - Only personal items are displayed</li>
        </ul>
        </td>
        <td> Pass </td>
    </tr>
    <tr>
        <td><strong>US006</strong></td>
        <td><strong>AS A</strong> logged in user <strong>I WANT TO</strong> update ingredient quantities <strong>SO THAT I CAN</strong> keep my pantry inventory accurate</td>
        <td>
            <ul>
                <li>Click on the edit button(pencil icon) on the pantry item card</li>
                <li>Update the quantity, units, or other details in the populated form</li>
                <li>Click Update button to confirm changes</li>
            </ul>
        </td>
        <td>
            <ul>
                <li>✅ Edit button is visible on each pantry item</li>
                <li>✅ Form pre-populates with current item values</li>
                <li>✅ Changes are saved and immediately reflected</li>
                <li>✅ Success message confirms update</li>
                <li>✅ Form validation prevents invalid entries</li>
            </ul>
        </td>
        <td> Pass </td>
    </tr>
    <tr>
        <td><strong>US007</strong></td>
        <td><strong>AS A</strong> logged in user <strong>I WANT TO</strong> delete items from my pantry <strong>SO THAT I CAN</strong> remove ingredients I no longer have</td>
        <td>
            <ul>
                <li>Click the Delete item button(bin icon) on pantry item card</li>
                <li>Click the Delete button in dialog to confirm deletion</li>
            </ul>
        </td>
        <td>
            <ul>
                <li>✅ Delete button/link is available for each pantry item</li>
                <li>✅ Confirmation dialog appears before deletion</li>
                <li>✅ User can confirm or cancel deletion</li>
                <li>✅ Item is permanently removed after confirmation</li>
                <li>✅ Confirmation message displayed after successful deletion</li>
                <li>✅ Pantry list updates immediately after deletion</li>
                <li>✅ Only item owner can delete their items</li>
                <li>✅ Deleted items cannot be recovered</li>
            </ul>
        </td>
        <td> Pass </td>
    </tr>
    <tr>
      <td><strong>US009</strong></td>
      <td><strong>AS A</strong> mobile user <strong>I WANT TO</strong> access basic pantry features on my phone <strong>SO THAT I CAN</strong> manage my pantry while shopping</td>
      <td>Check using Google Development tools</td>
      <td>Results in TODO </td>
      <td> Pass </td>
    </tr>
    <tr>
      <td><strong>US010</strong></td>
      <td><strong>AS A</strong> home cook <strong>I WANT TO</strong> find recipes using ingredients I have in my pantry <strong>SO THAT I CAN</strong> cook meals without additional shopping</td>
      <td>Test <code>RecipeSearchForm</code> and <code>SpoonacularApiService</code></td>
      <td>API integration with pantry matching working</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US011</strong></td>
      <td><strong>AS A</strong> cook <strong>I WANT TO</strong> see detailed recipe information including ingredients, instructions, and prep time <strong>SO THAT I CAN</strong> understand what's needed</td>
      <td>Test <code>recipe_detail</code> view with API data</td>
      <td>Detailed recipe view with ingredient comparison</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US012</strong></td>
      <td><strong>AS A</strong> home cook <strong>I WANT TO</strong> filter recipes by how many pantry ingredients they use <strong>SO THAT I CAN</strong> prioritize recipes requiring minimal shopping</td>
      <td>Test recipe filtering by matched ingredients count</td>
      <td>Recipe results show matched vs missing ingredients</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US013</strong></td>
      <td><strong>AS A</strong> cook <strong>I WANT TO</strong> save recipes I like to a favorites list <strong>SO THAT I CAN</strong> easily find them again for future cooking</td>
      <td>Test <code>recipe_save</code> function and <code>SavedRecipe</code> model</td>
      <td>Recipe saving with duplicate prevention working</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US014</strong></td>
      <td><strong>AS A</strong> cook <strong>I WANT TO</strong> see all my saved recipes in one place <strong>SO THAT I CAN</strong> browse my personal recipe collection</td>
      <td>Test saved recipes view in <code>recipes_list</code></td>
      <td>Saved recipes tab displaying user's collection</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US015</strong></td>
      <td><strong>AS A</strong> organized cook <strong>I WANT TO</strong> see a weekly meal calendar interface <strong>SO THAT I CAN</strong> plan my meals for the week ahead</td>
      <td>Test <code>meal_planning</code> view with FullCalendar integration</td>
      <td>Interactive calendar with meal slots implemented</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US016</strong></td>
      <td><strong>AS A</strong> meal planner <strong>I WANT TO</strong> add specific recipes to calendar days and meal times <strong>SO THAT I CAN</strong> organize my weekly cooking schedule</td>
      <td>Test <code>MealPlanItemForm</code> and <code>get_meal_plan</code></td>
      <td>Recipe assignment to calendar working</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US017</strong></td>
      <td><strong>AS A</strong> meal planner <strong>I WANT TO</strong> automatically generate shopping lists based on my planned meals <strong>SO THAT I CAN</strong> buy ingredients needed for my weekly menu</td>
      <td>Test <code>generate_shopping_list_items</code> function</td>
      <td>Shopping list generation from meal plans working</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US018</strong></td>
      <td><strong>AS A</strong> meal planner <strong>I WANT TO</strong> see which recipe ingredients I already have <strong>SO THAT I CAN</strong> only buy what I need</td>
      <td>Test pantry vs recipe ingredient comparison in <code>PantrySearch</code></td>
      <td>Ingredient matching logic separating needed vs available</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US019</strong></td>
      <td><strong>AS A</strong> shopper <strong>I WANT TO</strong> view and modify my generated shopping list <strong>SO THAT I CAN</strong> customize it before shopping</td>
      <td>Test <code>ShoppingListForm</code> and list editing</td>
      <td>Shopping list display and management working</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US020</strong></td>
      <td><strong>AS A</strong> user with many ingredients <strong>I WANT TO</strong> search my pantry by name <strong>SO THAT I CAN</strong> quickly find specific items</td>
      <td>Test search functionality in pantry views</td>
      <td>Search filtering implemented in pantry management</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US021</strong></td>
      <td><strong>AS A</strong> organized user <strong>I WANT TO</strong> view my pantry items organized by categories <strong>SO THAT I CAN</strong> easily find ingredients by type</td>
      <td>Test <code>Category</code> model and categorized display</td>
      <td>Category-based organization with <code>CATEGORY_CHOICES</code></td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US022</strong></td>
      <td><strong>AS A</strong> mobile user <strong>I WANT TO</strong> access all PantryPilot features on my phone <strong>SO THAT I CAN</strong> manage pantry, recipes, and meal planning while mobile</td>
      <td>Test full responsive design across all features</td>
      <td>Mobile-first responsive design implemented</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US023</strong></td>
      <td><strong>AS A</strong> cook <strong>I WANT TO</strong> remove recipes from my favorites list <strong>SO THAT I CAN</strong> keep my saved recipes relevant</td>
      <td>Test recipe deletion from saved collection</td>
      <td>Recipe removal functionality working</td>
      <td>✅ Pass</td>
    </tr>
    <tr>
      <td><strong>US024</strong></td>
      <td><strong>AS A</strong> cook <strong>I WANT TO</strong> search recipes by name, cuisine, or dietary restrictions <strong>SO THAT I CAN</strong> find specific types of meals</td>
      <td>Test advanced search filters in <code>RecipeSearchForm</code></td>
      <td>Cuisine, diet, and meal type filtering implemented</td>
      <td>✅ Pass</td>
    </tr>
  </tbody>
</table>

</details>




