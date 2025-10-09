from django.urls import path
from . import views

urlpatterns = [
    path(
        'category/<int:category_id>/delete',
        views.delete_category,
        name="category_delete"
    ),
    path(
        'item/<int:item_id>/delete',
        views.delete_pantry_item,
        name="pantry_item_delete"
    ),
    path(
        'item/<int:item_id>/update',
        views.update_pantry_item,
        name="pantry_item_update"
    ),
    path(
        'item/<int:item_id>/handle',
        views.resolve_duplicate_pantry_item,
        name="pantry_item_handle"
    ),
    path('', views.CategoryList.as_view(), name="pantry"),
]
