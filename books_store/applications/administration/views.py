from datetime import date, timedelta
#
from django.shortcuts import render, redirect
from django.views import View
#
from applications.order.models import Order
from applications.books.models import Book

class AdminView(View):

    template_name = 'administration/admin_panel.html'

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous):
            return redirect('home_app:home')
        if(self.request.user.ocupation != '0'):
            return render(request, 'generic/not_found.html')
        
        
        # get date range
        today = date.today()
        start_month = date(today.year, today.month, 1)
        end_month = start_month + timedelta(days=today.day)
    
        orders_by_month = Order.objects.get_sales_by_daterange(start_month, end_month).count()
        revenue_by_month = Order.objects.get_revenue_by_month(start_month, end_month)
        max_sale_by_month = Order.objects.get_highest_sale_by_month(start_month, end_month)
        out_of_stock_books = Book.objects.get_books_out_of_stock()
        orders_of_month = Order.objects.get_sales_by_daterange(start_month, end_month)

        print(max_sale_by_month)

        return render(request, self.template_name, {
            'current_month_orders':orders_by_month,
            'revenue_of_month':revenue_by_month,
            'max_sale_by_month':max_sale_by_month,
            'out_of_stock_books':out_of_stock_books,
            'orders_of_month':orders_of_month
        })


