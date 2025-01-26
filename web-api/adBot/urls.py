from django.urls import path , include

from .views import *

urlpatterns = [
    path('home' , homeView , name='home'),
]
