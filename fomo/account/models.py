from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

# Create your models here.
class FomoUser(AbstractUser):
    ## inheriting from super
    # id
    # first_name
    # last_name
    # username
    # email
    #password
    birthday = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length = 20)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    zipcode = models.CharField(max_length = 50)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
