from django.urls import path
#
from .views import (
        OrderDetails, 
        MyOrders, 
        AllOrders, 
        PendingOrdersView,
        ModifyOrder
    )

app_name = 'order'

urlpatterns = [
    path(
        'order/order-details/<orderId>',
        OrderDetails.as_view(),
        name='order-details'
    ),
    path(
        'order/my-orders',
        MyOrders.as_view(),
        name='my-orders'
    ),
    path(
        'order/all-orders',
        AllOrders.as_view(),
        name='all-orders'
    ),
    path(
        'order/pending-orders',
        PendingOrdersView.as_view(),
        name='pending-orders'
    ),
    path(
        'order/update-order/<orderId>',
        ModifyOrder.as_view(),
        name='update-order'
    )
]