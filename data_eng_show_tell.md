# Data Engineering Show & Tell

# ![PantryPilot Responsive Mockup](documentation/screenshots/pantry_pilot_amiresponsive.png)


> ## 🍽️ Can I make dinner with what I've already got?
>
> *A simple question that becomes an interesting data problem.*

<br>
 
## 🤔 The problem

Imagine I have got:
<table>
  <tr>
    <td><strong>My Pantry</strong></td>
    <td><strong>Online Recipe Ingredients</strong></td>
  </tr>

  <tr>
    <td>🍅 Tomatoes</td>
    <td>🍅 Fresh tomatoes</td>
  </tr>

  <tr>
    <td>🫘 Chickpeas</td>
    <td>🫘 Chickpeas</td>
  </tr>

  <tr>
    <td>🍚 Rice</td>
    <td>🍚 White rice</td>
  </tr>

  <tr>
    <td>🧅 Onions</td>
    <td>🌱 Spring onions</td>
  </tr>

  <tr>
    <td>🥬 Spinach</td>
    <td>🧄 Garlic</td>
  </tr>
</table>

Now, before I start cooking, there's one thing I really want to know:

> **Can I actually make this with what I've already got?**

And if I can't:

> **What do I need to buy?**

**`That's the idea behind PantryPilot.`**

<br>

But underneath this simple question is a data-engineering problem:

> **`How do I take data from different sources, structure it, clean it, match it, and turn it into something useful?`**

The answer to the simple question involves:

- Modelling my pantry data in a structured database
- Fetching and transforming recipe data from an external API
- Storing the recipe and ingredient data I need
- Matching saved recipe ingredients against my pantry
- Generating a shopping list from the ingredients I don't have

<br>

## ⚡ So what did I build?

**`PantryPilot`**

• full-stack pantry management application

Features: 

• `pantry management` • `discover recipes` • `plan meals` • `generate shopping lists`

### 🛠️ Tech Stack

| Technology | Why I used it |
|---|---|
| **Python / Django** | Build the backend and structure the application around reusable models and views |
| **PostgreSQL** | Store structured relational data such as users, pantry items, recipes and ingredients |
| **Spoonacular API** | Provide recipe data without having to build and maintain my own recipe database |
| **RapidFuzz** | Compare differently named ingredients when matching saved recipes against pantry items |
| **HTML / CSS / JavaScript** | Build the user-facing application |
| **Heroku** | Deploy the finished application |

### 🔑 Core Goals

- Model pantry and recipe data in a structured relational database
- Integrate and transform data from an external API
- Match ingredients that may be represented differently
- Turn the processed data into useful shopping-list information
- Build a complete application that could be extended further

<br>

## The Data Flow

PantryPilot brings together recipe data from Spoonacular API with pantry and saved recipe data stored in PostgreSQL.

- 🌐 Recipe search → recipes are retrieved from external Spoonacular API
- 💾 Save recipe → the selected recipe and its ingredients are stored in PostgreSQL
- 🥫 Pantry data → user's ingredients are stored in PostgreSQL

Pantry and saved recipe data are compared through the ingredient-matching process.
- 🧹 Normalisation → saved recipe ingredients are cleaned before comparison
- 🥊 Matching → RapidFuzz compares saved recipe ingredients with pantry items

The result is:
- 🛒 Derived data → a shopping list containing the ingredients needed to make the selected recipe.

<figure>
  <img src="documentation/data_flow.png" 
       alt="Data flow diagram" 
       width="100%" 
       style="max-width: 900px; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 20px 0;">
</figure>

> **Note:** Spoonacular provides its own matched/missing ingredient information for recipe search results. PantryPilot's RapidFuzz matching is used later when comparing **saved recipe ingredients with pantry items**.

<br>

## 🗃️ Giving the Ingredients a Home

The first step was figuring out how to represent all of the different pieces of information.

`Users`, `pantry items`, `saved recipes`, `recipe ingredients` and `shopping lists`, are all modelled separately and connected through relationships.

### Entity Relationship Diagram(ERD)

<figure>
  <img src="documentation/erd_pantry_pilot_color.png" 
       alt="ERD showing database relationships" 
       width="100%" 
       style="max-width: 900px; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 20px 0;">
</figure>

This relational structure means the data has relationships rather than being one large collection of text.

For example:

```text
User
 │
 ├── PantryItem
 │      ├── Tomatoes
 │      ├── Chickpeas
 │      └── Rice
 │
 └── SavedRecipe
        │
        └── RecipeIngredient
               ├── Tomatoes
               ├── Chickpeas
               └── Garlic
```

### Why this matters

This makes the data:

- structured
- queryable
- connected through relationships
- easier to validate
- easier to extend later

<br>


## 🐍 From ERD to Python

The ERD became Django models backed by PostgreSQL.
- [`pantry/models.py`](./pantry/models.py)
- [`recipe/models.py`](./recipe/models.py)

For example, a pantry item contains structured fields rather than just a name:

```python
class PantryItem(models.Model):
    """
    Stores a single pantry item with quantity and units
    related to :model:`auth.User` and :model:`Category`
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pantry_items"
    )
    name = models.CharField("Item", max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.CharField(
        max_length=20, choices=constants.UNIT_CHOICES, default='piece'
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="pantry_items"
    )
    image = CloudinaryField('image', default="placeholder", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
```

The important idea here is:

```text
Ingredient
   │
   ├── name
   ├── quantity
   ├── units
   ├── category
   └── user
```

It's not just storing information - the information has **`structure` and `meaning`**.

<br>

## 🌐 Bringing in Data From Outside

The next piece is the recipe data.

> PantryPilot uses the **`Spoonacular API`** as an external recipe data source.

The application makes an API request, receives the recipe information, and then reshapes that response into something it can actually use.



### Service layer:
[`recipe/spoonacular.py`](./recipe/spoonacular.py)

• `make the API request` • `handle errors` • `receive the external response` • `transform it into the application's structure`

The API response is formatted into fields the application can work with, including:

```text
Recipe
├── API recipe ID
├── Title
├── Matched ingredients
├── Missing ingredients
├── Matched ingredient count
└── Missing ingredient count
```
<br>

> **Note**
> - One useful thing Spoonacular gives is its own **matched and missing ingredient information** for recipe search results.
> - So the application doesn't need to run its own matching algorithm just to display those search results.
> - But once a user saves a recipe, its ingredients are stored in the database — and that's where it's own matching logic comes in.

<br>

## 🧩 Are These Actually the Same Ingredient?

This is probably the most interesting data problem in the project.

By this point, there are two sets of structured data in the database:
- 🥫 Ingredients in the user's pantry
- 🍽️ Ingredients from a saved recipe

Now a deceptively simple question needs to be answered:

> **Are these actually the same ingredient?**

Here's where things get interesting.

```text
🌐 Spoonacular
      │
      ▼
  Recipe Search
      │
      ▼
 User saves recipe
      │
      ▼
🗃️ PostgreSQL
      │
      │
      ├───────────────┐
      │               │
      ▼               ▼
Saved Recipe       🥫 Pantry
Ingredients           │
      │               │
      └───────┬───────┘
              ▼
       🥊 Ingredient Matching
              │
              ▼
        🛒 Shopping List
```
For example, my pantry might contain:

**`Tomatoes`**

while the saved recipe contains:

**`Fresh tomatoes`**

When compared directly these two strings are different.

```python
"fresh tomatoes" == "tomatoes"

False
```

But to a person, they're referring to the same ingredient for this particular use case.

So a better way to compare ingredient names is key requirement.

<br>

### 🧹 Step One: Normalising the data

Before comparing the ingredients, the names are normalised for consistency by handling things like:

- capitalisation
- whitespace
- unnecessary descriptive words


[`pantry/pantry_search.py`](./pantry/pantry_search.py)

```python
# Normalize the arguments for better matching
        normalized_pantry = {
            self._normalize(item.name): item
            for item in pantry_items
        }
```

```python
for recipe_ingredient in recipe_ingredients:
            if isinstance(recipe_ingredient, dict):
                normalized_ingredient = self._normalize(
                    recipe_ingredient['name']
                )
```

Conceptually:

```text
" Fresh   Tomatoes "
          │
          ▼
"fresh tomatoes"
```

This means comparing cleaner data rather than whatever wording happened to come from the API.

<br>

### 🥊 Step Two: Fuzzy Matching


Normalisation helps, but it doesn't solve everything.

PantryPilot uses **RapidFuzz** to calculate how similar two ingredient names are.

Instead of requiring an exact text match, I get a **similarity score** and use thresholds to decide whether something looks like a good match.

Conceptually:

```text
Saved recipe ingredient
          │
          ▼
      Normalise
          │
          ▼
   Compare with pantry
          │
          ▼
    Similarity score
       ↙       ↘
    Match     No match
```

[`pantry/pantry_search.py`](./pantry/pantry_search.py)

```python
class PantrySearchConfig:
    """
    Configuration settings for the searches.
    - This centralizes all the configuration settings in one place
    """
    
    # Threshold value for matching(must be >= the value)
    MATCH_THRESHOLD = 75        # to filter matched ingredients
    SIMILAR_THRESHOLD = 70      # to filter similar ingredients

    # Number of best matches to return
    MATCH_LIMIT = 2
```

```python
# Use process.extract to get best matches
process.extract(
    query=normalized_ingredient,
    choices=pantry_names,
    scorer=fuzz.token_set_ratio,
    limit=PantrySearchConfig.MATCH_LIMIT,
    score_cutoff=PantrySearchConfig.SIMILAR_THRESHOLD
)
```

For example:

```text
"tomato"      → "tomatoes"       → likely match
"chickpea"    → "chickpeas"      → likely match
"fresh rice"  → "rice"           → likely match
```

This is a useful example of **entity resolution**:

> Working out whether two differently written records refer to the same real-world thing.

<br>

### ⚠️ But There's a Catch...


Consider:

- **`onion`**  
- **`spring onion`**

These are clearly similar words, so a fuzzy matching algorithm might give them a pretty good score.

> But should the application really tell the user they already have what they need?

**Not necessarily.**

And that's the interesting part.

This isn't just a question of finding similar strings. It's about really trying to work out whether **two records represent the same thing for my particular domain**.

That's where the **data-quality and entity-resolution** side of the problem comes in.

<br>

## 🛒 Turning Data Into Something Useful

Once those comparisons have been made, something useful can actually be done with them.

Let's say the saved recipe has five ingredients and we've managed to match three of them to things in the pantry.

```text
🍅 Tomatoes       ✓
🫘 Chickpeas      ✓
🍚 Rice           ✓
🧄 Garlic         ✗
🌿 Basil          ✗
```

That leaves us with two ingredients that we probably need to buy.

[`shopping/views.py`](./shopping/views.py)

The shopping list is therefore **`derived data`** — information created from the pantry, saved recipe and matching results.

> `I'm taking the data I've already got, processing it, and producing something useful from it.
This is the point where the data stops being interesting just because it's structured, and actually becomes useful to the person using the application.`

<br>


## 🚀 What I'd Do Next

There are a couple of things I'd improve if I continued developing this.

The biggest one would probably be the ingredient matching.

At the moment, I'm largely working with the words themselves. But I've been learning about semantic search, and I think that could be a really interesting next step here.

Instead of only asking how similar two pieces of text are, I could represent ingredients based on their meaning and use that to find likely matches.

```text
Ingredient
     │
     ▼
 Embedding
     │
     ▼
Semantic search
     │
     ▼
Possible matches
     │
     ▼
Domain rules
     │
     ▼
Final decision
```

I wouldn't rely on semantic search by itself, though.

The onion and spring onion example is a good reason why. Two things can be very closely related semantically without being interchangeable.

So I'd probably combine semantic search with a canonical ingredient database and some rules specific to the food domain.


## 🎯 8. Why This Is Relevant to Data Engineering

And that's really why I think this project is useful for demonstrating my data engineering skills.

The application itself is a food application, but the problems underneath it are much more general.

I'm bringing data in from an external source, deciding how to model it, cleaning it up, comparing records from different sources, dealing with imperfect data, and then producing something useful from the result.

If this grew into a much larger application, I'd probably separate the external data ingestion from the main application as well — so I'd have something more like raw data coming in, then validation and cleaning, then structured data that the application and analytics could use.

```text
External Sources
       │
       ▼
   Raw Data
       │
       ▼
Validation & Cleaning
       │
       ▼
Structured Data
       │
   ┌───┴───┐
   ▼       ▼
Application Analytics
```

> **The main thing I took away from building PantryPilot is that putting data into a database is only the starting point.**
>
> **The more interesting challenge is making data from different sources reliable, comparable and useful.**
