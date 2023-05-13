from django.urls import path
#
from .views import (
            BookDetails, 
            BooksByCategory, 
            AllBooks, 
            AllBooksAdmin,
            UpdateBook,
            CreateBook,
            MarkOutOfStockBook)

app_name = 'books'

urlpatterns = [
    path(
        'books/details/<bookId>',
        BookDetails.as_view(),
        name='book-details'
    ),
    path(
        'books/category/<categoryId>',
        BooksByCategory.as_view(),
        name='book-category'
    ),
    path(
        'books/all-books',
        AllBooks.as_view(),
        name='all-books'
    ),
    path(
        'books/my-books',
        AllBooksAdmin.as_view(),
        name='my-books'
    ),
    path(
        'books/update-book/<pk>',
        UpdateBook.as_view(),
        name='update-book'
    ),
    path(
        'books/create-book',
        CreateBook.as_view(),
        name='create-book'
    ),
    path(
        'books/no-stock',
        MarkOutOfStockBook.as_view(),
        name='no-stock'
    )
]