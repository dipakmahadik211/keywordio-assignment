from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your views here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
       
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser  = True
        user.save(using=self._db)
        return user


class Useradmins(AbstractBaseUser):
   
    username = None
    full_name = models.CharField(max_length=250,blank=True,null=True)
    email = models.EmailField(max_length=50,unique=True,blank=True,null=True,verbose_name='email address') 
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)    
    is_superuser = models.BooleanField(default=True)                     
    last_login = models.DateTimeField(blank=True, null=True, verbose_name='last login')
    created_at = models.DateTimeField(auto_now_add=True)
    created_ip_address = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    modified_ip_address = models.CharField(max_length=50)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'useradmins'

    def __str__(self):
        return self.email