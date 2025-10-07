from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_list, name='shopping'),
    path(
        '<int:shopping_list_id>/',
        views.shopping_list,
        name='shopping_detail'
    ),
    path(
        '<int:shopping_list_id>/delete',
        views.delete_shopping_list,
        name='delete_shopping_list'
    ),
]
