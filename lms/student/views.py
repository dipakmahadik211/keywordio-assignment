from re import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views import View
from lmsadmin.models.books import Books

# Create your views here.
class BookView(View):
    
    def get(self,request):
        books_list = Books.get_books_list()
        template = loader.get_template('student-books/books-list.html')
        return HttpResponse(template.render({'book_list':books_list},request))
