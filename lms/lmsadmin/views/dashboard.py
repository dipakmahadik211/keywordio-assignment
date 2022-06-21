from re import template
from django.shortcuts import redirect, render
from django.template import loader
from django.views import View
from django.http import HttpResponse
# Create your views here.

class Dashboard(View):
    
    def get(self,request):
        template = loader.get_template('dashboard/dashboard.html')
        return HttpResponse(template.render({},request))
    
   