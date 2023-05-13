from django.db import models
from model_utils.models import TimeStampedModel
#
from applications.books.models import Book
from applications.carshop.models import Car
from applications.users.models import User, Address
from .managers import OrdersManager

class PaymentMethod(models.Model):

    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'PaymentMethod'
        verbose_name_plural = 'PaymentMethods'
    
    def __str__(self):
        return str(self.id)+' - '+self.name

class Order(TimeStampedModel):

    STATUS_ORDER = [
        ('r', 'Ready to Delivery'),
        ('d', 'On Route'),
        ('dch', 'Delivered Charge'),
        ('c', 'Completed')
    ]

    created_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField()
    phone= models.CharField(max_length=30)
    postcode = models.CharField(max_length=30)
    address1 = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address1')
    address2 = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address2')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=4, choices=STATUS_ORDER, default='r')

    objects = OrdersManager()

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return str(self.id)+' - '+str(self.total)

class OrderItem(models.Model):

    book = models.ForeignKey(Book,on_delete=models.CASCADE, related_name='book_order')
    quantity = models.PositiveIntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_orderitem')
    revenue = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'
    
    def __str__(self):
        return str(self.order.id)+' - '+str(self.book.id)+' - '+str(self.sub_total)


