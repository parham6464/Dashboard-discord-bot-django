from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    discord_id = models.CharField(max_length=255 , null=True , blank=True)
    discord_tag = models.CharField(max_length=255 , null=True)
    avatar = models.CharField(max_length=255 , null=True)
    public_flags = models.IntegerField( null=True)
    flags = models.IntegerField( null=True)
    locale= models.CharField(max_length=255 , null=True)  
    mfa_enabled = models.BooleanField( null=True)
    last_login = models.DateTimeField(auto_now=True , null=True)
    
