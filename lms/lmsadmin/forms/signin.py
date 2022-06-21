from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from lmsadmin.models.auth import Useradmins

class SignInForm(forms.Form):
    email = forms.CharField(error_messages = {'required': 'Email is required.'},widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    password = forms.CharField(error_messages = {'required': 'Password is required.'},widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = Useradmins.objects.get(email=email)              
            return user
        except Useradmins.DoesNotExist:
            raise ValidationError('Please enter a valid email.')