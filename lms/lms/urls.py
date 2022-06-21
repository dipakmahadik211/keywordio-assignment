from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lms-admin/', include('lmsadmin.urls')),
  #  path('lms-admin/', include('student.urls')),
]
