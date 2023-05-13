from django.shortcuts import render, redirect
from django.views import View
#
from applications.books.models import Book
from .models import WishList, WishListitem

class MyWishListView(View):

    template_name = 'wishlist/my_wishlist.html'

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous):
            return redirect('/')
        
        # find user wishlist
        wishlist = WishList.objects.filter(user=self.request.user).first()

        if wishlist is None:
            # create a wishlist
            new_wishlist = WishList()
            new_wishlist.user = self.request.user
            new_wishlist.save()

            return render(request, self.template_name,{
                'wishlist_items':None,
                'total_items': 0
            })
        else:
            # find products of wishlist
            wishlist_items = WishListitem.objects.filter(
                wishlist=wishlist
            ).order_by('-id')

            total_items = wishlist_items.count()

            return render(request, self.template_name,{
                'wishlist_items': wishlist_items,
                'total_items': total_items
            })

class AddItemToWishList(View):

    def post(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous):
            return redirect('/auth/login')
        
        # verify if user already has a wishlist
        wishlist = WishList.objects.filter(user=self.request.user).first()

        if wishlist is None:
            new_wishlist = WishList()
            new_wishlist.user = self.request.user
            new_wishlist.save()
            wishlist = WishList.objects.filter(user=self.request.user).first()
        
        # verify if book is not in wishlist yet
        book_id = self.request.POST.get('book_id')
        book = Book.objects.get(id=book_id)
        wishlist_item = WishListitem.objects.filter(book=book).first()

        if wishlist_item is not None:
            return redirect('wishlist:my-wishlist')
        
        # add item
        new_wishlist_item = WishListitem()
        new_wishlist_item.book = book
        new_wishlist_item.wishlist = wishlist
        new_wishlist_item.save()

        return redirect('wishlist:my-wishlist')

class RemoveItemFormWishlist(View):

    def post(self, request, *args, **kwargs):

        if(self.request.user.is_anonymous):
            return redirect('/auth/login')
        
        wishlist = WishList.objects.filter(user=self.request.user).first()

        wishlist_item_id = self.request.POST.get('wl_item_id')

        # find item
        wishlist_item = WishListitem.objects.filter(
            wishlist=wishlist,
            id=wishlist_item_id
        ).first()

        if wishlist_item_id is None:
            return redirect('/')
        
        wishlist_item.delete()

        return redirect('wishlist:my-wishlist')
        
