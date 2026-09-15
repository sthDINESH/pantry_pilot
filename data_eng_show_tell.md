# Data Engineering Show & Tell
<br>

> ## 🍽️ Can I make dinner with what I've already got?
>
> *A simple question that becomes an interesting data problem.*

<br>
 
## 1. The problem

**PantryPilot** is a smart pantry management application, but underneath the user-facing features is a small data engineering problem.

<br>

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

But once I started building it, I realised there was a much more interesting problem underneath that simple question: 
- my pantry data is in my database
- the recipe information is coming from an external API
- once a recipe is saved, I then need to compare those recipe ingredients against what's actually in my pantry
- and generate shopping list for items I needed to buy.

<br>

This is a data-engineering problem:

> **`How do I take data from different sources, structure it, clean it, match it, and turn it into something useful?`**

<br>

## 2. The Data Flow

PantryPilot brings together recipe data from Spoonacular with pantry and saved recipe data stored in PostgreSQL.

- 🌐 Recipe search → recipes are retrieved from Spoonacular
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

## 3. Giving the Ingredients a Home

The first step was figuring out how to represent all of this information.

`Users`, `pantry items`, `saved recipes`, `recipe ingredients` and `shopping lists`, are all modelled separately and connected through relationships.

### Entity Relationship Diagram(ERD)

<figure>
  <img src="documentation/erd_pantry_pilot_color.png" 
       alt="ERD showing database relationships" 
       width="100%" 
       style="max-width: 900px; height: auto; border: 1px solid #ddd; border-radius: 8px; margin: 20px 0;">
</figure>

This structure means the data has relationships rather than being one large collection of text.

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


# 4. From ERD to Python

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

I'm not just storing information.

I'm giving the information **`structure` and `meaning`**.

<br>

## 5. 🌐 Bringing in Data From Outside

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

# 6. The Interesting Problem: Are These the Same Ingredient?

This became the most interesting data problem in the project.

> Once a recipe has been saved, I need to compare its ingredients against the ingredients in the user's pantry.

For example:

**My database:**  
`Tomatoes`

**Saved recipe:**  
`Fresh tomatoes`

If I compare those two strings directly, they're different.

```python
"fresh tomatoes" == "tomatoes"

False
```

But if I showed them to a person, most people would immediately understand that they're referring to the same ingredient for this particular use case.

So I needed a way to compare ingredient names.


### 🧹 Step One: Normalisation

Before comparing the ingredients, I clean the names.

The project has a `_normalize()` function which:

- converts text to lowercase
- removes unnecessary whitespace
- removes configured ignore terms
- makes the strings more consistent

Conceptually:

```text
" Fresh   Tomatoes "
          │
          ▼
"fresh tomatoes"
```

This means I'm comparing cleaner data rather than whatever wording happened to come from the API.

---

### 🥊 Step Two: Fuzzy Matching

Normalisation helps, but it doesn't solve everything.

So PantryPilot uses **RapidFuzz** to calculate how similar two ingredient names are.

Conceptually:

```text
Recipe ingredient
       │
       ▼
   Normalise
       │
       ▼
  RapidFuzz
       │
       ▼
Similarity score
       │
       ▼
 ┌─────┴─────┐
 │           │
Match     No Match
```

The implementation uses:

```python
process.extract(
    query=normalized_ingredient,
    choices=pantry_names,
    scorer=fuzz.token_set_ratio,
    limit=PantrySearchConfig.MATCH_LIMIT,
    score_cutoff=PantrySearchConfig.SIMILAR_THRESHOLD
)
```

Then a threshold is used to decide whether the result is considered a match.

For example:

```text
"tomato"      → "tomatoes"       → likely match
"chickpea"    → "chickpeas"      → likely match
"fresh rice"  → "rice"           → likely match
```

This is a useful example of **entity resolution**:

> Working out whether two differently written records refer to the same real-world thing.

<br>

###. The Catch: when **`onion` meets `spring onion`**

This is also where I discovered an important limitation.

Consider:

```text
"onion"
"spring onion"
```

A fuzzy matching algorithm can tell me that the words are similar.

But similarity doesn't necessarily mean:

> "These ingredients are interchangeable."

That's an important **data quality problem**.

The current system therefore uses a relatively simple approach:

```text
Text
 ↓
Normalisation
 ↓
Fuzzy similarity
 ↓
Threshold
 ↓
Match / No Match
```

It's useful, but it isn't perfect.

And that's actually one of the things I would improve.

<br>

## 7. Turning Data Into Something Useful

Once I've made those comparisons, I can actually do something useful with them.

Let's say the saved recipe has five ingredients and I've managed to match three of them to things in the pantry.

```text
🍅 Tomatoes       ✓
🫘 Chickpeas      ✓
🍚 Rice           ✓
🧄 Garlic         ✗
🌿 Basil          ✗
```

That leaves me with two ingredients that I probably need to buy.

[`shopping/views.py`](./shopping/views.py)

The shopping list is therefore **derived data** — information created from the pantry, saved recipe and matching results.

I'm taking the data I've already got, processing it, and producing something useful from it.

This is the point where the data stops being interesting just because it's structured, and actually becomes useful to the person using the application.

<br>

## 8. 🚀 What I'd Do Next

## 🚀 7. What I'd Do Next

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
