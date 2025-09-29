from django.urls import path
from . import views

urlpatterns = [
    path('recipe/<int:recipe_id>', views.recipe_detail, name='recipe_detail'),
    path('recipe/<int:recipe_id>/save', views.recipe_save, name='recipe_save'),
    path('', views.recipes_list, name='recipes'),
]
