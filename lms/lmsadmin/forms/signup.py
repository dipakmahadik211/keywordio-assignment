from dataclasses import fields
from tkinter import Widget
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from lmsadmin.models.auth import Useradmins

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Useradmins
        fields = ['email', 'password']
        widgets = {
            'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'})
        }
        error_messages = {
            'email':{
                'required':'Email is required.'
            },
            'password':{
                'required':'Password is required.'
            },
        }
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = Useradmins.objects.get(email=email)              
            raise ValidationError('Email already exists.')
        except Useradmins.DoesNotExist:
            return email
            