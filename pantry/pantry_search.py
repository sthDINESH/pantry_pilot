import re
from rapidfuzz import fuzz, process

# =============================================================================
# CONFIGURATION SETTINGS
# =============================================================================


class PantrySearchConfig:
    """
    Configuration settings for the searches.
    - This centralizes all the configuration settings in one place
    """
    # List of regex strings to match against items and ignore for normalization
    IGNORE_TERMS = [
        r'\b(fresh|dried|chopped|sliced|diced|minced|grated|ground)\b',
        r'\b(organic|free-range|extra virgin|virgin)\b',
        r'\b(large|medium|small|whole|half)\b',
        r'\b(cups?|tbsp|tsp|oz|lbs?|grams?|kg)\b',
        r'\b(red|green|yellow|orange|purple|brown)\b',
        r'\b(bell|fuji|bramley|braeburn)\b',
        r'\b(pink|blue|dark|light|golden|pale)\b',
        r'\d+(\.\d+)?',  # Remove numbers
        r'[^\w\s]',  # Remove punctuation
    ]

    # Threshold value for matching(must be >= the value)
    MATCH_THRESHOLD = 75        # to filter matched ingredients
    SIMILAR_THRESHOLD = 70      # to filter similar ingredients

    # Number of best matches to return
    MATCH_LIMIT = 2


class PantrySearch:
    """
    Class that implements the methods for searching and matching
    against
    Uses rapidFuzz library for fuzzy matching
    """
    def find_match(self, recipe_ingredients, pantry_items):
        """
        Match recipe ingredients with pantry_items using rapidFuzz

        Params:
        - recipe_ingredients ([]) : iterable of query objects for
          recipe ingredients
        - pantry_items ([]) : iterable of query objects for pantry_items
        Returns:
        - matched_ingredients: List of tuples
          (recipe_ingredient, pantry_item, score)
        - similar_ingredients: List of tuples
          (recipe_ingredient, pantry_item, score)
        - missing_ingredients: List of recipe ingredients not found in pantry
        """
        matched_ingredients = []
        similar_ingredients = []
        missing_ingredients = []

        # Normalize the arguments for better matching
        normalized_pantry = {
            self._normalize(item.name): item
            for item in pantry_items
        }
        pantry_names = list(normalized_pantry.keys())

        for recipe_ingredient in recipe_ingredients:
            if isinstance(recipe_ingredient, dict):
                normalized_ingredient = self._normalize(
                    recipe_ingredient['name']
                )
            else:
                normalized_ingredient = self._normalize(
                    recipe_ingredient.ingredient_name
                )

            if not normalized_ingredient:
                missing_ingredients.append(recipe_ingredient)
                continue

            # Use process.extract to get best matches
            matches = process.extract(
                query=normalized_ingredient,
                choices=pantry_names,
                scorer=fuzz.token_set_ratio,
                limit=PantrySearchConfig.MATCH_LIMIT,
                score_cutoff=PantrySearchConfig.SIMILAR_THRESHOLD,
            )

            number_matches = len(matches)
            if number_matches:
                print("***", recipe_ingredient, matches)
                for match in matches:
                    matched_name, score, _ = match
                    pantry_item = normalized_pantry[matched_name]
                    if score >= PantrySearchConfig.MATCH_THRESHOLD:
                        matched_ingredients.append(
                            (
                                recipe_ingredient,
                                pantry_item,
                                score
                            )
                        )
                        continue
                    else:
                        # Record this as missing
                        missing_ingredients.append(recipe_ingredient)
                        # But also note this as similar items
                        similar_ingredients.append(
                            (recipe_ingredient, pantry_item, score)
                        )
            else:
                missing_ingredients.append(recipe_ingredient)
        return matched_ingredients, similar_ingredients, missing_ingredients

    # -------------------------------------------------------------------------
    # Private helper methods
    # -------------------------------------------------------------------------
    def _normalize(self, name):
        """
        Normalize ingredient name for better matching

        Params:
            name (str) Ingredient/item string
        Returns:
            normalized (str) : string with irrelevant terms and spaces removed
        """
        if not name:
            return ""

        # Convert to lowercase and remove extra whitespace
        normalized = re.sub(r'\s+', ' ', name.lower().strip())

        # Remove common cooking terms and quantities
        for pattern in PantrySearchConfig.IGNORE_TERMS:
            normalized = re.sub(pattern, '', normalized)

        return re.sub(r'\s+', ' ', normalized).strip()
