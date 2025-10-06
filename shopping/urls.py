from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_list, name='shopping'),
    path(
        '<int:shopping_list_id>/',
        views.shopping_list,
        name='shopping_detail'
    ),
]
