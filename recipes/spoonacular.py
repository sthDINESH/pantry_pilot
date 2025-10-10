from django.conf import settings
from django.utils.html import strip_tags
import logging
from typing import List, Dict
import requests

import recipes.api_response as api_response
import config.constants as constants

# =============================================================================
# CONFIGURATION SETTINGS
# =============================================================================


class APIConfig:
    """
    Configuration settings for the external recipe API service.
    - This centralizes all the configuration settings for API in one place
    - Supports different limits for different types of operations
    """

    # Spoonacular API configuration
    SPOONACULAR_BASE_URL = "https://api.spoonacular.com/recipes"
    SPOONACULAR_API_KEY = (
        settings.SPOONACULAR_API_KEY  # From environment variables
    )

    # Test with dummy response
    MOCK_API_CALL = False


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
                'message': (
                    'External recipe service temporarily unavailable. '
                    'Please try again later.'
                ),
                'fallback_suggestions': self._get_fallback_suggestions(
                    ingredients
                ),
                # 'quota_status': self.quota_manager.get_user_quota_status(
                #     user_id
                # )
            }

    def get_recipe_details(self, recipe_id: str, user_id: int) -> Dict:
        """
        Get detailed information for a specific recipe.
        - Get full recipe details
        - Used when user clicks on a recipe to see instructions, etc.
        """
        # Make API call
        api_result = self._get_recipe_details_from_api(recipe_id)

        if api_result['success']:
            return {
                'success': True,
                'source': 'api',
                'recipe': api_result['recipe'],
            }
        else:
            return {
                'success': False,
                'error': api_result['error'],
                'message': 'Recipe details temporarily unavailable.',
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
                response = requests.get(
                    "https://dog.ceo/api/breeds/image/random",
                    timeout=30
                )

            if response.status_code == 200:
                if not APIConfig.MOCK_API_CALL:
                    recipes_data = response.json()
                else:
                    recipes_data = api_response.example_recipes_search_response
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
                            (
                                f'API request failed with status '
                                f'{response.status_code}'
                            )
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

    def _get_recipe_details_from_api(self, recipe_id: str) -> Dict:
        """Get detailed recipe information from Spoonacular API."""
        try:
            url = f"{APIConfig.SPOONACULAR_BASE_URL}/{recipe_id}/information"
            params = {
                'apiKey': APIConfig.SPOONACULAR_API_KEY,
                'includeNutrition': False,  # costs extra API points
                'addWinePairing': False,  # costs extra API points
                'addTasteData': False,  # costs extra API points
            }

            # Make the API call
            if not APIConfig.MOCK_API_CALL:
                response = requests.get(url, params=params, timeout=30)
            else:
                response = requests.get(
                    "https://dog.ceo/api/breeds/image/random",
                    timeout=30
                )

            if response.status_code == 200:
                if not APIConfig.MOCK_API_CALL:
                    recipe_data = response.json()
                else:
                    recipe_data = api_response.example_recipe_detail_response
                return {
                    'success': True,
                    'recipe': self._format_recipe_details(recipe_data)
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
                    'message': 'Failed to get recipe details'
                }
        except Exception as e:
            self.logger.error(f"Error getting recipe details: {e}")
            return {
                'success': False,
                'error': 'NETWORK_ERROR',
                'message': 'Failed to retrieve recipe details'
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
                'api_recipe_id': recipe.get('id'),
                'title': recipe.get('title'),
                'image': self._correct_image_url(recipe.get('image')),
                'matched_ingredients_count': recipe.get('usedIngredientCount'),
                'missing_ingredients_count': (
                    recipe.get('missedIngredientCount')
                ),
                'matched_ingredients': [
                    ing.get('name')
                    for ing in recipe.get('usedIngredients', [])
                ],
                'missing_ingredients': [
                    ing.get('name')
                    for ing in recipe.get('missedIngredients', [])
                ],
                'source': 'spoonacular'
            }
            formatted_recipes.append(formatted_recipe)
        return formatted_recipes

    def _format_recipe_details(self, raw_data: Dict) -> Dict:
        """Convert detailed recipe data to standard format."""
        return {
            'is_external': True,
            'api_recipe_id': raw_data.get('id'),
            'title': raw_data.get('title'),
            'api_image_url': self._correct_image_url(raw_data.get('image')),
            'summary': strip_tags(raw_data.get('summary', '')),
            'cook_time': raw_data.get('readyInMinutes'),
            'servings': raw_data.get('servings'),
            'instructions': self._format_analyzed_instructions(
                raw_data.get('analyzedInstructions')
            ),
            'ingredients': [
                {
                    'name': ing.get('name'),
                    'original_name': ing.get('original'),
                    'amount': ing.get('amount'),
                    'unit': (
                        (
                            ing.get('unit').lower()
                            if ing.get('unit').lower() in [
                                unit[0] for unit in constants.UNIT_CHOICES
                            ]
                            else 'piece'
                        )
                    ),
                    'note': (
                        " ".join(ing.get('meta'))
                        if ing.get('meta') else ""
                    ),
                    'metric': ing.get('measures').get('metric'),
                }
                for ing in raw_data.get('extendedIngredients', [])
            ],
            'api_source_url': raw_data.get('sourceUrl'),
            'source': 'spoonacular'
        }

    def _format_analyzed_instructions(self, raw_data: List) -> str:
        """
        Covert analyzedInstructions field of recipe details response
        to standard format
        """
        html_ol = ""
        html_li = ""
        for step in raw_data[0]["steps"]:
            html_li += f"<li>{step["step"]}</li>"
        html_ol = f"<ol>{html_li}</ol>"

        return html_ol

    def _correct_image_url(self, raw_data: str) -> str:
        """
        Correct the image url if needed
        Some api responses seem to have image extensions missing
        """
        if not raw_data:
            return raw_data

        # Check if URL ends with a period (indicating missing extension)
        if raw_data.endswith('.'):
            # Add default .jpg extension for Spoonacular recipe images
            return raw_data + 'jpg'

        # Return original URL if it appears to be properly formatted
        return raw_data
