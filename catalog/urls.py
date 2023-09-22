from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),

    # we could also use re_path() below, which uses regex to match a pattern
    # an example would be re_path(r'^book/(?P<pk>\d+)$'
    # all regex must contain r'' with the content between the '
    # ^ matches the start of the text while $ matches the end of it
    # book/ matches the text "book/"
    # (?P<pk>\d+) is more complex. (?P<name>...) captures the pattern noted
    # at ..., and names the matched pattern "name". The name is passed to the view
    # with that name specified. \d captures all digits
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('staffbooks/', views.LoanedBooksByUserLibrarianListView.as_view(), name='staff-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]
