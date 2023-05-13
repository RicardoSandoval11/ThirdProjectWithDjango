from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    OCUPATION_CHOICES = [
        ('0', 'Administrator'),
        ('1', 'Worker'),
        ('2', 'Client'),
    ]

    email = models.CharField(max_length=200, unique=True)
    full_name = models.CharField(max_length=200)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    token = models.CharField(max_length=10, blank=True, null=True)
    ocupation = models.CharField(max_length=1, choices=OCUPATION_CHOICES, default='2')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [ 'full_name' ]

    objects = UserManager()

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.full_name

class Address(models.Model):

    default_address = models.CharField(max_length=200,blank=True)
    default_shipping_address = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='address')

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
    
    def __str__(self):
        return str(self.id)+' - '+self.default_shipping_address
