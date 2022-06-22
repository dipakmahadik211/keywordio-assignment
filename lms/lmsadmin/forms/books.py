from pyexpat import model
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from lmsadmin.models.books import Books

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['book_name', 'book_author', 'book_publication', 'book_price','book_image']    
        widgets = {
            'book_name':forms.TextInput(attrs={'class':'form-control'}),
            'book_author':forms.TextInput(attrs={'class':'form-control'}),
            'book_publication':forms.TextInput(attrs={'class':'form-control'}),
            'book_price':forms.NumberInput(attrs={'class':'form-control'}),
            'book_image':forms.FileInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'book_name':{
                'required':'Book name is required.'
            },
            'book_author':{
                'required':'Book author is required.'
            },
            'book_publication':{
                'required':'Book publication is required.'
            },
            'book_price':{
                'required':'Book price is required.'
            },
            'book_image':{
                'required':'Book image is required.'
            }
            
        }