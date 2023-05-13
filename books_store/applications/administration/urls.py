from django.urls import path
#
from .views import AdminView

app_name = 'admin_app'

urlpatterns = [
    path(
        'admin-panel/',
        AdminView.as_view(),
        name='admin-panel'
    )
]