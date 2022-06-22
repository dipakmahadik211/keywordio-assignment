from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from lmsadmin.middlewares.auth import auth_middleware
from lmsadmin.views.auth import Auth,SignUp,SignOut
from lmsadmin.views.books import BooksCreateView,BooksAjaxDatatableView,BooksEditView,BooksListView,BooksStatusView
from lmsadmin.views.dashboard import Dashboard

urlpatterns = [
    # Auth
    path('sign-in/', Auth.as_view(), name='lms-admin/sign-in'),
    path('sign-up/', SignUp.as_view(), name='lms-admin/sign-up'),
    path('sign-out/', SignOut.as_view(), name='lms-admin/sign-out'),
    # Auth
    
    # Books
    path('books-list/', auth_middleware(BooksListView.as_view()), name='lms-admin/books-list'),
    path('add-book/', auth_middleware(BooksCreateView.as_view()), name='lms-admin/add-book'),
    path('edit-book/<int:id>', auth_middleware(BooksEditView.as_view()), name='lms-admin/edit-book'),
    path('ajax-books-list/', auth_middleware(BooksAjaxDatatableView.as_view()), name='lms-admin/ajax-books-list'),
    path('books-change-status/', auth_middleware(BooksStatusView.as_view()), name='books-change-status'),
    # Books
    
    # Dashboard
    path('dashboard/', auth_middleware(Dashboard.as_view()), name='lms-admin/dashboard'),
    # Dashboard
    
]


if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
