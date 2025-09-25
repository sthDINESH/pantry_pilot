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