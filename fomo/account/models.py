from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class FomoUser(AbstractUser):
    # inheriting from super
    # id
    # first_name
    # last_name
    phone = models.CharField(max_length = 20)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    zipcode = models.CharField(max_length = 50)
