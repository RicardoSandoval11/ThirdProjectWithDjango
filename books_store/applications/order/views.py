import datetime
#
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
#
from .models import Order, OrderItem

class MyOrders(LoginRequiredMixin,ListView):

    template_name = 'orders/my_orders.html'
    paginate_by = 6
    context_object_name = 'orders'
    login_url = '/auth/login'

    def get_queryset(self):
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            orders = Order.objects.filter(created_at__range=(start_date,end_date)).order_by('-created_at')
        else:
            orders = Order.objects.filter(user=self.request.user).order_by('-created_at')
        return orders


class OrderDetails(View):

    template_name = 'orders/order_details.html'

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous):
            return redirect('/')
        
        orderId = self.kwargs['orderId']

        # find order
        order = Order.objects.get(id=orderId)

        if(self.request.user.id != order.user.id):
            return redirect('/')

        # find order items
        order_items = OrderItem.objects.filter(
            order=order
        )
        return render(request, self.template_name,{
            'order':order,
            'order_items':order_items
        })

class AllOrders(View):

    template_name = 'orders/all_orders.html'

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous or self.request.user.ocupation != '0'):
            return redirect('home_app:home')
        
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        if start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            orders = Order.objects.filter(created_at__range=(start_date,end_date)).order_by('-created_at')
        else:
            orders = Order.objects.filter(user=self.request.user).order_by('-created_at')

        paginator = Paginator(orders, 6)
        page = self.request.GET.get('page')
        objs_page = paginator.get_page(page)

        return render(request, self.template_name, {
            'page_obj':objs_page
        })

class PendingOrdersView(View):

    template_name = 'orders/pending_orders.html'

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous or self.request.user.ocupation != '0'):
            return redirect('home_app:home')
        
        orders = Order.objects.get_pending_orders()
        paginator = Paginator(orders, 6)
        page = self.request.GET.get('page')
        objs_page = paginator.get_page(page)

        return render(request, self.template_name, {
            'page_obj':objs_page
        })

class ModifyOrder(View):

    template_name = 'orders/modify_order.html'

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous or self.request.user.ocupation != '0'):
            return redirect('home_app:home')
        
        order_id = self.kwargs['orderId']

        order = Order.objects.get(id=order_id)
        
        return render(request, self.template_name, {
            'order_id':order_id,
            'current_status':order.order_status,
            'status_options': Order.STATUS_ORDER
        })

    def post(self, request, *args, **kwargs):
        order_id = self.request.POST.get('order_id')
        status = self.request.POST.get('order_status')

        order = Order.objects.get(id=order_id)
        if status is not None:
            order.order_status = status
            order.save()

        return redirect('order:pending-orders')