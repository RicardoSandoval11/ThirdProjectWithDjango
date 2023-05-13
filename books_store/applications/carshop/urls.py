from django.urls import path
#
from .views import (
    AddProductToCar,
    CheckOutView,
    ShowCarShop,
    RemoveCarShopItem
)

app_name = 'carshop'

urlpatterns = [
    path(
        'car/add-product',
        AddProductToCar.as_view(),
        name='add-product'
    ),
    path(
        'car/checkout',
        CheckOutView.as_view(),
        name='checkout'
    ),
    path(
        'car/my-carshop',
        ShowCarShop.as_view(),
        name='carshop'
    ),
    path(
        'car/remove-item',
        RemoveCarShopItem.as_view(),
        name='remove-item'
    )       
]