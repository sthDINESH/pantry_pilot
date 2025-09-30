from django.urls import path
from . import views

urlpatterns = [
    path(
        'recipe/<int:api_recipe_id>',
        views.recipe_detail,
        name='recipe_detail'
    ),
    path(
        'recipe/saved/<int:recipe_id>',
        views.saved_recipe_detail,
        name='saved_recipe_detail'
    ),
    path(
        'recipe/<int:api_recipe_id>/save',
        views.recipe_save,
        name='recipe_save'
    ),
    path(
        'recipe/<int:recipe_id>/delete',
        views.recipe_delete,
        name='recipe_delete'
    ),
    path('', views.recipes_list, name='recipes'),
]
