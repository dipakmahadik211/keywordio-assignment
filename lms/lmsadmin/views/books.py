from re import template
from django.shortcuts import redirect, render
from django.template import loader
from django.views import View
from django.http import HttpResponse
from lmsadmin.models.auth import Useradmins
from lmsadmin.models.books import Books
from ajax_datatable.views import AjaxDatatableView
# Create your views here.

class BooksListView(View):
    
    def get(self,request):
        template = loader.get_template('books/books-list.html')
        return HttpResponse(template.render({},request))
    
    
class BooksStatusView(View):
    
    def post(self,request):
        admin_id = request.session['admin_id']
        user = Useradmins.objects.get(id=admin_id) 
        id = request.POST.get('id')
        status = request.POST.get('status')
        state_obj = Books.objects.get(id=id)
        state_obj.status = status
        state_obj.modified_at = Books.now()
        state_obj.modified_by  = user
        state_obj.modified_ip_address = request.META.get('REMOTE_ADDR')
        state_obj.save()
        return HttpResponse(True)

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
                <i class="fa fa-toggle-on tgle-on" title="Active" data-url="cities-change-status/">
            """
        else:
             row['status'] = """
                <i class="fa fa-toggle-off tgle-off" title="Inactive" data-url="cities-change-status/">
            """
              
        row['Action'] = """
                <a class="btn-warning btn-xs edit-city" title="Edit"><i class="icon-pencil"></i></a>
                <a class="btn-danger btn-xs del-record" title="Delete" data-url="cities-change-status/"><i class="icon-trash"></i></a>
            """
    
    def get_initial_queryset(self, request=None):    
        return Books.objects.exclude(status='delete')
        
 
    
   