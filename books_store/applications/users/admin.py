from django.contrib import admin
#
from .models import User, Address

admin.site.register(Address)
admin.site.register(User)

