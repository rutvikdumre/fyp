from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class UserB2(models.Model):
    name = models.CharField(max_length=200,blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    history = models.JSONField(default=set)
    
class User(AbstractBaseUser):
    tid=models.CharField(max_length=200,blank=True) 