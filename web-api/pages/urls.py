from django.urls import path , include

from .views import *

urlpatterns = [
    path('home/' , Home.as_view() , name='Home'),

]
