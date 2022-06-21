from django.contrib import admin
from django.urls import path
from lmsadmin.views.auth import Auth,SignUp

urlpatterns = [
    path('sign-in/', Auth.as_view(), name='lms-admin/sign-in'),
    path('sign-up/', SignUp.as_view(), name='lms-admin/sign-up'),
]
