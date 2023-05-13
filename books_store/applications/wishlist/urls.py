from django.urls import path
#
from .views import (
        AddItemToWishList,
        MyWishListView,
        RemoveItemFormWishlist
    )

app_name = 'wishlist'

urlpatterns = [
    path(
        'wishlist/my-wishlist',
        MyWishListView.as_view(),
        name='my-wishlist'
    ),
    path(
        'wishlist/add-item',
        AddItemToWishList.as_view(),
        name='add-item'
    ),
    path(
        'wishlist/remove-item',
        RemoveItemFormWishlist.as_view(),
        name='remove-item'
    )
]