from django.shortcuts import render
from django.views.generic import TemplateView
#
from applications.categories.models import Category
from applications.books.models import Book

class HomeView(TemplateView):

    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_categories'] = Category.objects.get_most_popular_categories()
        context['recent_books_added'] = Book.objects.get_most_recent_books()
        context['most_sold_books'] = Book.objects.get_most_sold_books()
        context['most_popular_books'] = Book.objects.get_most_popular_books()
        return context

class NotFoundView(TemplateView):

    template_name = 'generic/not_found.html'
    
