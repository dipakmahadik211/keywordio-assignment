from datetime import datetime
from re import template
from django.shortcuts import redirect, render
from django.template import loader
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from lmsadmin.models.auth import Useradmins
from lmsadmin.models.books import Books
from lmsadmin.forms.books import BookForm
from ajax_datatable.views import AjaxDatatableView
# Create your views here.

class BooksListView(View):
    
    def get(self,request):
        template = loader.get_template('books/books-list.html')
        return HttpResponse(template.render({},request))


class BooksCreateView(View):
    
    def get(self,request):
        form = BookForm() 
        template = loader.get_template('books/create-new-book.html')
        return HttpResponse(template.render({'form':form},request))  
    
    def post(self,request):
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES)
            user = Useradmins.objects.get(id=request.session['admin_id'])  
            if form.is_valid():
                obj = form.save(commit=False)
                obj.created_by = user
                obj.created_on = datetime.now()
                obj.save()
                return HttpResponseRedirect('/lms-admin/books-list/')
            else:
                print(form.errors)
        else:
            form = BookForm() 
        template = loader.get_template('books/create-new-book.html')
        return HttpResponse(template.render({'form':form},request)) 
    
    
class BooksStatusView(View):
    
    def post(self,request):
        admin_id = request.session['admin_id']
        user = Useradmins.objects.get(id=admin_id) 
        id = request.POST.get('id')
        status = request.POST.get('status')
        obj = Books.objects.get(id=id)
        obj.status = status
        obj.modified_on = datetime.now()
        obj.modified_by  = user
        obj.save()
        return HttpResponse(True)

class BooksEditView(View):
    def get(self,request,id=None):
        if id is None:
            return redirect('/lms-admin/books-list/') 
        try:
            book_obj = Books.objects.get(id=id)
            form = BookForm(request.GET or None, instance=book_obj)
        except Books.DoesNotExist:
            return redirect('/lms-admin/books-list/')                            
        template = loader.get_template('books/edit-book.html')
        return HttpResponse(template.render({'form':form,'book_image':book_obj.book_image},request))
    
    def post(self,request,id=None):
        if request.method == 'POST':
            book_obj = Books.objects.get(id=id) 
            form = BookForm(request.POST,instance=book_obj)        
            if form.is_valid(): 
                user = Useradmins.objects.get(id=1)              
                obj = form.save(commit=False) 
                obj.modified_on = datetime.now()
                obj.modified_by  = user
                obj.save()
                return HttpResponseRedirect('/lms-admin/books-list/')
            else:
                print(form.errors)              
        else:
            form = BookForm()       
        template = loader.get_template('books/edit-book.html')
        return HttpResponse(template.render({'form':form},request))

class BooksAjaxDatatableView(AjaxDatatableView):

    model = Books
    title = 'Books List'
    initial_order = [["book_name", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100]]
    search_values_separator = '+'

    column_defs = [
       # AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': True, }, 
        {'name': 'book_name', 'visible': True, },
        {'name': 'book_author', 'visible': True, },
        {'name': 'book_price', 'visible': True, },
        {'name': 'status', 'visible': True, 'searchable': False, 'orderable': False, },
        {'name': 'Action', 'visible': True, 'searchable': False, 'orderable': False, },
    ]
    
    def customize_row(self, row, obj):
      
        if row['status'] == 'active':
            row['status'] = """
                <i class="fa fa-toggle-on tgle-on" title="Active" data-url="books-change-status/">
            """
        else:
             row['status'] = """
                <i class="fa fa-toggle-off tgle-off" title="Inactive" data-url="books-change-status/">
            """
              
        row['Action'] = """
                <a class="btn-warning btn-xs edit-books" title="Edit"><i class="fa fa-pencil"></i></a>
                <a class="btn-danger btn-xs del-record" title="Delete" data-url="books-change-status/"><i class="fa fa-trash"></i></a>
            """
    
    def get_initial_queryset(self, request=None):    
        return Books.objects.exclude(status='delete')
        
 
    
   