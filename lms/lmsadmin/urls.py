from django.contrib import admin
from django.urls import path
from lmsadmin.views.auth import Auth,SignUp
from lmsadmin.views.books import BooksAjaxDatatableView,BooksListView,BooksStatusView
from lmsadmin.views.dashboard import Dashboard

urlpatterns = [
    # Auth
    path('sign-in/', Auth.as_view(), name='lms-admin/sign-in'),
    path('sign-up/', SignUp.as_view(), name='lms-admin/sign-up'),
    # Auth
    
    # Books
    path('books-list/', BooksListView.as_view(), name='lms-admin/books-list'),
    path('ajax-books-list/', BooksAjaxDatatableView.as_view(), name='lms-admin/ajax-books-list'),
    path('books-change-status/', BooksStatusView.as_view(), name='books-change-status'),
    # Books
    
    # Dashboard
    path('dashboard/', Dashboard.as_view(), name='lms-admin/dashboard'),
    # Dashboard
    
]
