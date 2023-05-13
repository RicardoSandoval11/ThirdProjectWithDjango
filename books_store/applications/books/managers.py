from django.db import models
from django.db.models import Count
from itertools import chain

class BookManager(models.Manager):

    def get_authors(self):
        return self.raw('SELECT 1 as id, author FROM books_book GROUP BY author')

    def get_most_recent_books(self):
        return self.order_by('createdAt')[:4]
    
    def get_most_sold_books(self):
        return self.annotate(num_orders=Count('book_order')).order_by('-num_orders')[:4]
    
    def get_most_popular_books(self):
        return self.annotate(num_favorites=Count('favorite')).order_by('-num_favorites')[:4]
    
    def get_book_by_id(self, bookId):
        return self.filter(id=bookId).first()
    
    def get_related_books_by_category(self, category):
        return self.filter(category=category).order_by('-name')[:4]
    
    def get_books_by_category(self, category_id):
        return self.filter(category__id=category_id).order_by('-name')
    
    def get_books_by_kword(self, kword):
        return self.filter(name__icontains=kword)
    
    def get_books_by_author(self, author):
        return self.filter(author=author)
    
    def get_books_by_price_salary(self, low, top):
        offer_books = self.filter(
                                is_offer=True
                        ).filter(
                                offer_price__range=(low, top)
                        )
        normal_price_books = self.filter(is_offer=False).filter(sell_price__range=(low, top))
        result = list(chain(offer_books, normal_price_books))
        return result
    
    def get_books_by_price_salary_amount(self, low, top):
        offer_books = self.filter(
                                is_offer=True
                        ).filter(
                                offer_price__range=(low, top)
                        ).count()
        normal_price_books = self.filter(is_offer=False).filter(sell_price__range=(low, top)).count()
        result = offer_books + normal_price_books
        return result
    
    def get_books_out_of_stock(self):
        return self.filter(stock=0).count()