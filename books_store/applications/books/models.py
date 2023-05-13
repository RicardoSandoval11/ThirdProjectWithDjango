from django.db import models
from django.utils.timezone import now
#
from ckeditor_uploader.fields import RichTextUploadingField
#
from applications.categories.models import Category
from .managers import BookManager

class Book(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False)
    description = RichTextUploadingField('description')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_offer = models.BooleanField()
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    details = RichTextUploadingField('details')
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    author = models.CharField(max_length=200, blank=False)
    image = models.ImageField(upload_to='books', blank=False)
    createdAt = models.DateField(default=now)

    objects = BookManager()

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
    
    def __str__(self):
        return str(self.id)+' - '+self.name
