from django.db import models
#
from applications.books.models import Book
from applications.users.models import User

class WishList(models.Model):

    user = models.ForeignKey(
            User, 
            on_delete=models.CASCADE, 
            related_name='wishlist'
        )

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
    
    def __str__(self):
        return str(self.id)+' - '+self.user.full_name

class WishListitem(models.Model):

    book = models.ForeignKey(
            Book, 
            on_delete=models.CASCADE, 
            related_name='favorite'
    )
    wishlist = models.ForeignKey(
            WishList,
            on_delete=models.CASCADE,
            related_name='wishlist_item'
    )

    class Meta:
        verbose_name = 'WishListItem'
        verbose_name_plural = 'WishListItems'
    
    def __str__(self):
        return str(self.id)+' - '+self.book.name+' - '+str(self.wishlist.id)
