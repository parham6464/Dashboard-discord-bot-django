from django.shortcuts import render 
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpRequest , HttpResponse , JsonResponse
from django.shortcuts import redirect
import requests
from django.contrib.auth import authenticate , login
import string
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
# Create your views here.
# Create your views here.

def homeView(request):
    return render(request , 'index.html')
