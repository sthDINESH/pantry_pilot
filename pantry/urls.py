from django.urls import path
from . import views

urlpatterns = [
    path(
        '<int:item_id>/delete', 
        views.delete_pantry_item, 
        name="pantry_item_delete"
    ),
    path('', views.CategoryList.as_view(), name="pantry"),
]
