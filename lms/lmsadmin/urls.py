from django.contrib import admin
from django.urls import path
from lmsadmin.views.auth import Auth,SignUp
from lmsadmin.views.dashboard import Dashboard

urlpatterns = [
    # Auth
    path('sign-in/', Auth.as_view(), name='lms-admin/sign-in'),
    path('sign-up/', SignUp.as_view(), name='lms-admin/sign-up'),
    # Auth
    
    # Dashboard
    path('dashboard/', Dashboard.as_view(), name='lms-admin/dashboard'),
    # Dashboard
    
]
