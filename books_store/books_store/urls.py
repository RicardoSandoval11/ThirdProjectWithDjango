
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin-bookshop/', admin.site.urls),
    re_path('', include('applications.books.urls')),
    re_path('', include('applications.home.urls')),
    re_path('', include('applications.users.urls')),
    re_path('', include('applications.categories.urls')),
    re_path('', include('applications.carshop.urls')),
    re_path('', include('applications.order.urls')),
    re_path('', include('applications.wishlist.urls')),
    re_path('', include('applications.administration.urls')),
    # ckeditor
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
