import email
from django import views
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from django.views import View
from lmsadmin.models.auth import Useradmins
from lmsadmin.forms.signin import SignInForm
from lmsadmin.forms.signup import SignUpForm

# Create your views here.

class Auth(View):
    
    def get(self,request):
        form = SignInForm()
        template = loader.get_template('auth/sign-in.html') 
        return HttpResponse(template.render({'form':form},request))
    
    def post(self,request):
        if request.method == 'POST':
            form = SignInForm(request.POST)
            if form.is_valid():
                email = request.POST.get('email')
                password = request.POST.get('password')
                user = authenticate(email=email,password=password)
                if user is not None:                    
                    login(request,user)
                    request.session['admin_id'] = user.id
                    return HttpResponseRedirect('/lms-admin/dashboard/')             
            else:
                print(form.errors)
        else:
            form = SignInForm()
        template = loader.get_template('auth/sign-in.html') 
        return HttpResponse(template.render({'form':form},request))

class SignUp(View):
    
    def get(self,request):
        form = SignUpForm()
        template = loader.get_template('auth/sign-up.html') 
        return HttpResponse(template.render({'form':form},request))
    
    def post(self,request):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)     
                obj.username = request.POST.get('email')  
                obj.password = make_password(request.POST.get('password'))
                obj.save()                                 
            else:
                print(form.errors)
        else:
            form = SignUpForm()
        template = loader.get_template('auth/sign-up.html') 
        return HttpResponse(template.render({'form':form},request))
            
    
    