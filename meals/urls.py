from django.urls import path
from . import views

urlpatterns = [
    path('plan/', views.get_meal_plan, name='plan'),
    path(
        'delete/<int:meal_plan_item_id>/',
        views.delete_meal_plan_item,
        name='delete_meal_item'
    ),
    path(
        'update/<int:meal_plan_item_id>/',
        views.update_meal_plan_item,
        name='update_meal_item'
    ),
    path(
        'clear_selection/',
        views.clear_meal_selection,
        name='clear_selection'
    ),
    path('', views.meal_planning, name='meals'),
]
