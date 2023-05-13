from django.db import models
#
from applications.books.models import Book
from applications.users.models import User

class Car(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
    
    def __str__(self):
        return str(self.user.id)+' - '+str(self.total)

class CarShopItem(models.Model):

    book = models.ForeignKey(Book,on_delete=models.CASCADE, related_name='book')
    quantity = models.PositiveIntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'CarShopItem'
        verbose_name_plural = 'CarShopItems'
    
    def __str__(self):
        return str(self.car.id)+' - '+str(self.book.id)+' - '+str(self.sub_total)
