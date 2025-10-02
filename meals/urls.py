from django.urls import path
from . import views

urlpatterns = [
    path('plan/', views.get_meal_plan, name='plan'),
    path('', views.meal_planning, name='meals'),
]