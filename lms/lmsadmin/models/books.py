from random import choices
from django.db import models
from lmsadmin.models.auth import Useradmins

class Books(models.Model):
    
    StatusChoices = (
        ('active','active'),
        ('block','block'),
        ('delete','delete'),
    )
    
    id = models.BigAutoField(primary_key=True)
    book_name = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    book_publication = models.CharField(max_length=255)
    book_price = models.DecimalField(max_digits=5,decimal_places=2)
    created_by = models.ForeignKey(Useradmins,on_delete=models.CASCADE,related_name='book_created_by',db_column='created_by')
    created_on = models.DateTimeField(auto_created=True)
    modified_by = models.ForeignKey(Useradmins,on_delete=models.CASCADE,related_name='book_modified_by',db_column='modified_by')
    modified_on = models.DateTimeField(auto_created=True)
    status = models.CharField(max_length=255,choices=StatusChoices)
    
    class Meta:
        db_table = 'master_books'
    
    