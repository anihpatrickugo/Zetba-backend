from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class CustomUser(AbstractUser):
    phone = PhoneNumberField(blank=True, region="NG")
    balance = models.IntegerField(default=0)
    photo = models.ImageField(blank=True, null=True, upload_to='images/profile')

class Notifications(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title       = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    date        = models.DateField(auto_now_add=True)
    time        = models.TimeField(auto_now_add=True)
    read        = models.BooleanField(default=False)