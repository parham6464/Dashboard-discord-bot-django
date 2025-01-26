from django.urls import path , include

from .views import *

urlpatterns = [
    path('discord/login/' , discordLogin , name='discord_login'),
    path('discord/login/redirect' , successRedirect , name='success_redirect'),
    path('discord/profile/' , profileView , name='profileView'),

]
