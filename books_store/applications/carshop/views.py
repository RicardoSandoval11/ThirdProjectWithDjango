from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import FormView
#
from applications.order.models import Order, OrderItem
from applications.books.models import Book
from .forms import PlaceOrderForm
from .models import CarShopItem, Car

class AddProductToCar(View):

    def post(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous):
            return redirect('/auth/login')
        # verify if user already has a CarShop
        curr_car = Car.objects.filter(user=request.user).first()

        if curr_car is None:
            curr_car = Car()
            curr_car.user = request.user
            curr_car.total = 0.00
            curr_car.save()
            curr_car = Car.objects.get(user=request.user)

        # verify if the book has already added to the carshop
        book_id = self.request.POST.get('bookId')
        quantity = int(self.request.POST.get('quantity'))

        if(quantity == 0):
            return HttpResponseRedirect(redirect_to='/car/my-carshop')

        book_to_add = Book.objects.filter(id=book_id).first()
        
        car_item = CarShopItem.objects.filter(
            book=book_to_add,
            car=curr_car
        ).first()

        if car_item is None:
            new_car_item = CarShopItem()
            new_car_item.book = book_to_add
            new_car_item.car = curr_car
            if book_to_add.stock < quantity:
                quantity = book_to_add.stock
            new_car_item.quantity =  quantity
            if book_to_add.is_offer:
                new_car_item.sub_total = book_to_add.offer_price*quantity
            else:
                new_car_item.sub_total = book_to_add.sell_price*quantity
            # save item
            curr_car.total = curr_car.total + new_car_item.sub_total
            curr_car.save()
            new_car_item.save()
        else:
            if car_item.quantity + 1 <= book_to_add.stock:
                if book_to_add.is_offer:
                    curr_car.total = curr_car.total + quantity*book_to_add.offer_price
                else:
                    curr_car.total = curr_car.total + quantity*book_to_add.sell_price

            if car_item.quantity + quantity > book_to_add.stock:
                car_item.quantity = book_to_add.stock
                if book_to_add.is_offer:
                    car_item.sub_total = book_to_add.stock*book_to_add.offer_price
                else:
                    car_item.sub_total = book_to_add.stock*book_to_add.sell_price
            else:
                car_item.quantity = quantity + car_item.quantity
                if book_to_add.is_offer:
                    car_item.sub_total = car_item.quantity*book_to_add.offer_price
                else:
                    car_item.sub_total = car_item.quantity*book_to_add.sell_price

            curr_car.save()
            car_item.save()
        
        return HttpResponseRedirect(redirect_to='/car/my-carshop')

class ShowCarShop(View):

    template_name = 'carshop/my_carshop.html'

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous):
            return redirect('/auth/login')
        
        cart = Car.objects.filter(
            user=self.request.user
        ).first()

        if cart is not None:

            carshop_items = CarShopItem.objects.filter(
                car=cart
            ).order_by('-id')

            return render(request, self.template_name,{
                    'carshop_items':carshop_items, 
                    'total_items': carshop_items.count(), 
                    'cart':cart, 
                    'total':cart.total+20
                })
        else:
            return render(request, self.template_name,{
                    'carshop_items':None, 
                    'total_items': 0, 
                    'cart':cart, 
                    'total':None
                })

class RemoveCarShopItem(View):

    def post(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous):
            return HttpResponseRedirect('/')
        caritem_id = self.request.POST.get('carshop_item_id')
        # find item
        cart_item = CarShopItem.objects.get(id=caritem_id)
        # find cart
        cart = Car.objects.get(id=cart_item.car.id)

        cart_item.quantity = cart_item.quantity - 1

        all = self.request.POST.get('all')

        if all is not None:
            if cart_item.book.is_offer:
                cart.total = cart.total - (cart_item.quantity+1)*cart_item.book.offer_price
            else:
                cart.total = cart.total - (cart_item.quantity+1)*cart_item.book.sell_price
            
            cart_item.delete()
            cart.save()

            return HttpResponseRedirect('/car/my-carshop')

        if cart_item.quantity  == 0:
            cart.total = cart.total - cart_item.sub_total
            cart_item.delete()
        else:
            if cart_item.book.is_offer:
                cart_item.sub_total = cart_item.sub_total - cart_item.book.offer_price
                cart.total = cart.total - cart_item.book.offer_price
                cart_item.save()
                
            else:
                cart_item.sub_total = cart_item.sub_total - cart_item.book.sell_price
                cart.total = cart.total - cart_item.book.sell_price
                cart_item.save()
        cart.save()

        return HttpResponseRedirect('/car/my-carshop')

class CheckOutView(FormView):

    template_name = 'carshop/checkout.html'
    form_class = PlaceOrderForm

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous):
            return redirect('/')
        
        cart = Car.objects.filter(
            user=self.request.user
        ).first()


        carshop_items = CarShopItem.objects.filter(
            car=cart
        ).order_by('-id')

        return render(request, self.template_name,{
                'carshop_items':carshop_items, 
                'total_items': carshop_items.count(), 
                'cart':cart, 
                'total':cart.total+20,
                'form': self.form_class(user_id=self.request.user.id)
            })
    
    def form_valid(self, form):
        cart = Car.objects.filter(
            user=self.request.user
        ).first()

        carshop_items = CarShopItem.objects.filter(
            car=cart
        )

        # save order
        new_order = Order()

        new_order.created_at = timezone.now()
        new_order.user = self.request.user
        new_order.total = 0
        new_order.comment = form.cleaned_data['comment']
        new_order.phone = form.cleaned_data['phone']
        new_order.postcode = form.cleaned_data['postcode']
        new_order.address1 = form.cleaned_data['address1']
        new_order.address2 = form.cleaned_data['address2']
        new_order.payment_method = form.cleaned_data['payment_method']
        
        new_order.save()

        order_created = Order.objects.filter(
            user=self.request.user
        ).order_by('-created_at').first()

        # save each item of the order
        order_items = []
        for carshop_item in carshop_items:
            order_item = OrderItem()
            order_item.book = carshop_item.book

            # decrease the stock of each book
            book = Book.objects.filter(
                id=carshop_item.book.id
            ).first()

            if(carshop_item.quantity > book.stock):
                order_item.quantity = book.stock
                if(book.is_offer):
                    order_item.sub_total = book.stock * book.offer_price
                else:
                    order_item.sub_total = book.stock * book.sell_price
                book.stock = 0
                book.save()
            else:
                order_item.quantity = carshop_item.quantity
                order_item.sub_total = carshop_item.sub_total
                book.stock = book.stock - carshop_item.quantity
                book.save()    
            new_order.total = new_order.total + order_item.sub_total
            order_item.order = order_created
            order_item.revenue = order_item.sub_total - order_item.quantity*order_item.book.purchase_price
            order_items.append(order_item)
        new_order.total = new_order.total + 20
        new_order.save()
        
        OrderItem.objects.bulk_create(order_items)

        # remove items from carshop 
        CarShopItem.objects.filter(
            car=cart
        ).delete()

        # set the total amount of the cart to zero
        cart.total = 0
        cart.save()

        return redirect('order:order-details',orderId=order_created.id)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs




