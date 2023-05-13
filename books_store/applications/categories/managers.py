from django.db import models
from django.db.models import Q, Count

class CategoryManager(models.Manager):

    def get_most_popular_categories(self):
        return self.raw('SELECT * FROM categories_category WHERE id IN (SELECT category_id FROM books_book GROUP BY category_id ORDER BY COUNT(category_id) DESC LIMIT 6)')
    
    def get_all_categories(self):
        return self.all()
    
    def get_categories_by_kword(self, kword):
        return self.filter(
            Q(name__icontains=kword) | Q(description__icontains=kword)
        ).annotate(number_of_books=Count('category'))
    
    def get_all_categories(self):
        return self.all().annotate(number_of_books=Count('category'))