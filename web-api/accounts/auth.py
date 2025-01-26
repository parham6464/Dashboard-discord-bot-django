from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import CustomUser


class discordAuthBackend(BaseBackend):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, discord_id=None):
        
        try:
            login_valid = CustomUser.objects.get(discord_id=discord_id)
        except:
            return None
        if login_valid:
            try:
                user = CustomUser.objects.get(discord_id=discord_id)
                return user
            except:
                return None
        

    def get_user(self, discord_id):
        try:
            return CustomUser.objects.get(discord_id=discord_id)
        except CustomUser.DoesNotExist:
            return None
