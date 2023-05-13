from django.urls import path
#
from .views import (
            AllCategories, 
            AllCategoriesAdmin, 
            DeleteCategory,
            CreateCategoryView,
            UpdateCategoryView
        )

app_name = 'categories'

urlpatterns = [
    path(
        'categories/all',
        AllCategories.as_view(),
        name='all-categories'
    ),
    path(
        'categories/all-categories-admin',
        AllCategoriesAdmin.as_view(),
        name='all-categories-admin'
    ),
    path(
        'categories/delete-category',
        DeleteCategory.as_view(),
        name='delete-category'
    ),
    path(
        'categories/create-category',
        CreateCategoryView.as_view(),
        name='create-category'
    ),
    path(
        'categories/update-category/<pk>',
        UpdateCategoryView.as_view(),
        name='update-category'
    )
]
