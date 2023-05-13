from django.db import models
from django.db.models import Sum, Max, Q


class OrdersManager(models.Manager):

    def get_sales_by_daterange(self, start_date, end_date):
        return self.filter(created_at__range=(start_date, end_date)).annotate(revenue=Sum('order_orderitem__revenue'))

    def get_revenue_by_month(self, start_date, end_date):
        queryset = self.filter(created_at__range=(start_date, end_date)).annotate(revenue=Sum('order_orderitem__revenue'))
        return queryset.aggregate(total=Sum('revenue'))['total']
    
    def get_highest_sale_by_month(self, start_date, end_date):
        queryset = self.filter(created_at__range=(start_date, end_date))
        return queryset.aggregate(max_sale=Max('total'))['max_sale']
    
    def get_pending_orders(self):
        return self.filter(~Q(order_status='c'))
    