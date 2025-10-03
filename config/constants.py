UNIT_CHOICES = [
        # Weight measurements
        ('kg', 'Kilograms'),
        ('g', 'Grams'),
        ('lb', 'Pounds'),
        ('oz', 'Ounces'),

        # Volume measurements - Metric
        ('l', 'Liters'),
        ('ml', 'Milliliters'),

        # Volume measurements - Imperial/US
        ('cup', 'Cups'),
        ('cups', 'Cups'),
        ('servings', 'Servings'),
        ('tbsp', 'Tablespoons'),
        ('tsp', 'Teaspoons'),
        ('fl_oz', 'Fluid Ounces'),
        ('pt', 'Pints'),
        ('qt', 'Quarts'),
        ('gal', 'Gallons'),

        # Count/Piece measurements
        ('piece', 'Pieces'),
        ('item', 'Items'),
        ('can', 'Cans'),
        ('bottle', 'Bottles'),
        ('jar', 'Jars'),
        ('bag', 'Bags'),
        ('box', 'Boxes'),
        ('pack', 'Packs'),
        ('bunch', 'Bunches'),
        ('head', 'Heads'),
        ('clove', 'Cloves'),
        ('slice', 'Slices'),

        # Special measurements
        ('pinch', 'Pinches'),
        ('dash', 'Dashes'),
        ('drop', 'Drops'),
        ('serving', 'Servings'),
        ('portion', 'Portions'),
    ]

TIME_UNIT_CHOICES = [
    ('min', 'Minutes'),
    ('hr', 'Hours'),
    ('day', 'Days'),
]

STATUS_CHOICES = (
    (0, "Draft"), 
    (1, "Published")
)

# Additional cuisine choices for recipe filtering
CUISINE_CHOICES = [
    ('african', 'African'),
    ('american', 'American'),
    ('british', 'British'),
    ('cajun', 'Cajun'),
    ('caribbean', 'Caribbean'),
    ('chinese', 'Chinese'),
    ('eastern_european', 'Eastern European'),
    ('european', 'European'),
    ('french', 'French'),
    ('german', 'German'),
    ('greek', 'Greek'),
    ('indian', 'Indian'),
    ('irish', 'Irish'),
    ('italian', 'Italian'),
    ('japanese', 'Japanese'),
    ('jewish', 'Jewish'),
    ('korean', 'Korean'),
    ('latin_american', 'Latin American'),
    ('mediterranean', 'Mediterranean'),
    ('mexican', 'Mexican'),
    ('middle_eastern', 'Middle Eastern'),
    ('nordic', 'Nordic'),
    ('southern', 'Southern'),
    ('spanish', 'Spanish'),
    ('thai', 'Thai'),
    ('vietnamese', 'Vietnamese'),
]

# Additional diet choices for recipe filtering
DIET_CHOICES = [
    ('gluten_free', 'Gluten Free'),
    ('ketogenic', 'Ketogenic'),
    ('vegetarian', 'Vegetarian'),
    ('lacto_vegetarian', 'Lacto-Vegetarian'),
    ('ovo_vegetarian', 'Ovo-Vegetarian'),
    ('vegan', 'Vegan'),
    ('pescetarian', 'Pescetarian'),
    ('paleo', 'Paleo'),
    ('primal', 'Primal'),
    ('low_fodmap', 'Low FODMAP'),
    ('whole30', 'Whole30'),
]

"""
Meal type choices for recipe search
Supported types with Spoonacular recipe search API
"""

MEAL_TYPE_CHOICES = [
    ('main_course', 'Main Course'),
    ('side_dish', 'Side Dish'),
    ('dessert', 'Dessert'),
    ('appetizer', 'Appetizer'),
    ('salad', 'Salad'),
    ('bread', 'Bread'),
    ('breakfast', 'Breakfast'),
    ('soup', 'Soup'),
    ('beverage', 'Beverage'),
    ('sauce', 'Sauce'),
    ('marinade', 'Marinade'),
    ('fingerfood', 'Finger Food'),
    ('snack', 'Snack'),
    ('drink', 'Drink'),
]

"""
Meal category choices for meal planning
Used by :model:`MealPlanItem` to provides choices
for meal categories
"""
MEAL_PLAN_CATEGORIES = [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('snack', 'Snack'),
    ('appetiser','Appetiser'),
    ('dessert', 'Dessert'),
    ('brunch', 'Brunch'),
    ('other', 'Other'),
]