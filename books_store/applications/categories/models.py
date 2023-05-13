from django.db import models
#
from .managers import CategoryManager

class Category(models.Model):

    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories')
    description = models.TextField()

    objects = CategoryManager()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return str(self.id)+' - '+self.name

