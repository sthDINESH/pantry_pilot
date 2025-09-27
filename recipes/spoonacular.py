from django.conf import settings
import logging
from typing import List, Dict
import requests

import recipes.api_response as api_response

# =============================================================================
# CONFIGURATION SETTINGS
# =============================================================================


class APIConfig:
    """
    Configuration settings for the external recipe API service.
    - This centralizes all the configuration settings for API in one place
    - Supports different limits for different types of operations
    """

    # Daily limits per user (conservative to support multiple users)
    # DAILY_USER_LIMITS = {
    #     'recipe_searches': 10,    # Max 10 searches per user per day
    #     'recipe_details': 15,     # Max 15 detailed views per user per day
    # }

    # Application-wide limits (Spoonacular free tier)
    # DAILY_APP_LIMIT = 150        # Total requests per day for entire app

    # Cache timeouts (in seconds)
    # CACHE_TIMEOUTS = {
    #     'recipe_search': 86400,      # 24 hours for search results
    #     'recipe_details': 604800,    # 7 days for detailed recipe info
    #     'popular_searches': 172800,  # 48 hours for popular combinations
    #     'user_quota': 3600,         # 1 hour for user quota info
    # }

    # Spoonacular API configuration
    SPOONACULAR_BASE_URL = "https://api.spoonacular.com/recipes"
    SPOONACULAR_API_KEY = settings.SPOONACULAR_API_KEY  # From environment variables

    # Test with dummy response
    MOCK_API_CALL = True


# =============================================================================
# SPOONACULAR API SERVICE HANDLER
# =============================================================================


class SpoonacularApiService:
    """
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def search_recipes(
            self,
            ingredients: List[str],
            cuisine: str,
            diet: str,
            meal_type: str
         ) -> Dict:
        # Make API call
        api_result = self._make_spoonacular_api_call(
            cuisine=cuisine,
            diet=diet,
            meal_type=meal_type,
            ingredients=ingredients,
        )
        if api_result['success']:
            return {
                'success': True,
                'source': 'api',
                'recipes': api_result['recipes'],
                'total_results': len(api_result['recipes']),
            }
        else:
            # API call failed - return error with fallback options
            # self._update_analytics('api_error')
            return {
                'success': False,
                'error': api_result['error'],
                'message': 'External recipe service temporarily unavailable. Please try again later.',
                'fallback_suggestions': self._get_fallback_suggestions(ingredients),
                # 'quota_status': self.quota_manager.get_user_quota_status(user_id)
            }

    # =========================================================================
    # PRIVATE HELPER METHODS
    # =========================================================================
    def _make_spoonacular_api_call(
        self,
        ingredients: List[str],
        cuisine: str,
        diet: str,
        meal_type: str
    ) -> Dict:
        """
        Make the actual call to Spoonacular search recipes API.
        - This does the actual HTTP request to Spoonacular's servers
        - Handles network errors, API errors, and response parsing
        - Returns standardized response format regardless of what happens
        """
        try:
            url = f"{APIConfig.SPOONACULAR_BASE_URL}/complexSearch"
            params = {
                'apiKey': APIConfig.SPOONACULAR_API_KEY,
                'includeIngredients': ','.join(ingredients),
                'cuisine': cuisine,
                'diet': diet,
                'type': meal_type,
                'sort': 'max-used-ingredients',
                'fillIngredients': True,
                'number': 10,  # Number of recipes to return
                'ignorePantry': True  # Don't assume basic pantry items
            }

            params['cuisine'] = cuisine if cuisine else None
            params['diet'] = diet if diet else None
            params['type'] = meal_type if meal_type else None

            # Make the API call
            if not APIConfig.MOCK_API_CALL:
                response = requests.get(url, params=params, timeout=30)
            else:
                response = requests.get("https://dog.ceo/api/breeds/image/random", timeout=30)

            if response.status_code == 200:
                if not APIConfig.MOCK_API_CALL:
                    recipes_data = response.json()
                else:
                    recipes_data = api_response.api_response
                return {
                    'success': True,
                    'recipes': self._format_recipe_results(recipes_data)
                }
            elif response.status_code == 402:
                # Payment required - quota exceeded
                return {
                    'success': False,
                    'error': 'API_QUOTA_EXCEEDED',
                    'message': 'Daily API quota exceeded'
                }
            else:
                return {
                    'success': False,
                    'error': f'API_ERROR_{response.status_code}',
                    'message': (
                        (
                            f'API request failed with status {response.status_code}'
                        )
                    )
                }
        except requests.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return {
                'success': False,
                'error': 'NETWORK_ERROR',
                'message': 'Network error occurred while fetching recipes'
            }
        except Exception as e:
            self.logger.error(f"Unexpected error in API call: {e}")
            return {
                'success': False,
                'error': 'UNKNOWN_ERROR',
                'message': 'Unexpected error occurred'
            }

    def _format_recipe_results(self, raw_data: Dict) -> List[Dict]:
        """
        Convert Spoonacular complex recipe API response to standard format.
        - External API returns JSON data
        - Standardize it to match frontend expectations
        """
        formatted_recipes = []

        for recipe in raw_data['results']:
            formatted_recipe = {
                'id': recipe.get('id'),
                'title': recipe.get('title'),
                'image': recipe.get('image'),
                'used_ingredient_count': recipe.get('usedIngredientCount'),
                'missed_ingredient_count': recipe.get('missedIngredientCount'),
                'used_ingredient_names': [ing.get('name') for ing in recipe.get('usedIngredients', [])],
                'missed_ingredient_names': [ing.get('name') for ing in recipe.get('missedIngredients', [])],
                'source': 'spoonacular'
            }
            formatted_recipes.append(formatted_recipe)
        return formatted_recipes


if __name__ == "__main__":
    APIConfig.MOCK_API_CALL = True
    print(SpoonacularApiService().search_recipes(
        ingredients=['cheese', 'tomatoes', 'potatoes', 'salt', 'milk', 'onions'],
        cuisine="european",
        diet="vegetarian",
        meal_type='',
    ))
