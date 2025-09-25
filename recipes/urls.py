from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipes_list, name='recipes'),
]