from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .manager import UserManager
import datetime
from datetime import datetime, timedelta



def getTimeAfter1Min():
    now = datetime.now()
    now_plus_1 = now + timedelta(minutes = 1)
    return now_plus_1

class User(AbstractUser):
    username = None
    email = models.EmailField( unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=200 , null=True, blank=True)
    otp_expired_at = models.DateTimeField(default=getTimeAfter1Min)    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    #objects = UserManager()
    
#    def name(self):
#       return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email


