import datetime
#
from typing import Any
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
#
from applications.carshop.models import CarShopItem, Car
from applications.categories.models import Category
from .forms import CreateBookForm
from .mixins import AdminPermissionMixin
from .models import Book

class BookDetails(View):

    template_name = 'books/book_details.html'

    def get(self, request, *args, **kwargs):

        bookId = self.kwargs['bookId']

        book = Book.objects.get_book_by_id(bookId)

        if book is None:
            return render(request, 'generic/not_found.html')
        
        # related books by category
        category = Category.objects.get(id=book.category.id)

        related_books = Book.objects.get_related_books_by_category(category)

        return render(request, self.template_name,{'book':book, 'related_books':related_books})

class BooksByCategory(ListView):

    paginate_by = 6
    context_object_name = 'books'
    template_name = 'books/books_by_category.html'

    def get_queryset(self):
        category_id = self.kwargs['categoryId']

        # verify category exists
        category = Category.objects.filter(id=category_id).first()
        if(category is None):
            return redirect('/')
        books = Book.objects.get_books_by_category(category_id)
        return books

class AllBooks(ListView):

    paginate_by = 6
    context_object_name = 'books'
    template_name = 'books/all_books.html'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        filter_type = self.request.GET.get('filter_by')
        value = self.request.GET.get('value')

        context['categories'] = Category.objects.all()
        context['authors'] = Book.objects.get_authors()
        context['filter_by'] = filter_type
        context['value'] = value

        # price ranges
        price_ranges = []
        for i in range(0,500, 50):
            price_ranges.append({'value':str(i)+'-'+str(i+50)})
        
        context['prices'] = price_ranges

        if(filter_type == 'name'):
            context['total_elements'] = Book.objects.get_books_by_kword(value).count()
        elif(filter_type == 'author'):
            context['total_elements'] = Book.objects.get_books_by_author(value).count()
        elif(filter_type == 'price'):
            values = value.split('-')
            values[0] = float(values[0])
            values[1] = float(values[1])
            context['total_elements'] = Book.objects.get_books_by_price_salary_amount(values[0], values[1])
        elif(filter_type == 'category'):
            context['total_elements'] = Book.objects.get_books_by_category(value).count()
        else:
            context['total_elements'] = Book.objects.all().count()
        
        return context

    def get_queryset(self):
        filter_type = self.request.GET.get('filter_by')
        value = self.request.GET.get('value')

        if(filter_type == 'name'):
            return Book.objects.get_books_by_kword(value)
        elif(filter_type == 'author'):
            return Book.objects.get_books_by_author(value)
        elif(filter_type == 'price'):
            values = value.split('-')
            values[0] = float(values[0])
            values[1] = float(values[1])
            return Book.objects.get_books_by_price_salary(values[0], values[1])
        elif(filter_type == 'category'):
            return Book.objects.get_books_by_category(value)
        else:
            return Book.objects.all()

class AllBooksAdmin(View):

    template_name = 'books/all_books_admin.html'

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous or self.request.user.ocupation != '0'):
            return redirect('/')
        books = Book.objects.all()
        paginator = Paginator(books, 6)
        page = self.request.GET.get('page')
        objs_page = paginator.get_page(page)

        return render(request, self.template_name, {
            'books': books,
            'page_obj':objs_page
        })

class UpdateBook(AdminPermissionMixin, UpdateView):

    template_name = 'books/book_form.html'
    form_class = CreateBookForm
    success_url = reverse_lazy('books:my-books')
    model = Book

class CreateBook(CreateView):
    
    template_name = 'books/create_book.html'
    form_class = CreateBookForm
    success_url = reverse_lazy('books:my-books')

    def get(self, request, *args, **kwargs):
        if(self.request.user.is_anonymous or self.request.user.ocupation != '0'):
            return redirect('/')

        return render(request, self.template_name, {'form': self.form_class})

class MarkOutOfStockBook(AdminPermissionMixin, View):

    def post(self, request, *args, **kwargs):

        book_id = self.request.POST.get('book_id')

        book = Book.objects.get(id=book_id)

        # remove from all carts
        cartitems = CarShopItem.objects.filter(book=book)
        cartItemsToRemove = []
        for cartItem in cartitems:
            cart = Car.objects.get(id=cartItem.car.id)
            cart.total = cart.total - cartItem.sub_total
            cart.save()
            cartItemsToRemove.append(cartItem)
        CarShopItem.objects.filter(book=book).delete()
        book.stock = 0
        book.save()
        return redirect('books:my-books')
    



