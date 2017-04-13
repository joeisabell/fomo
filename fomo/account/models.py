from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

from fomo.methods import geocode_address as geo
from catalog import models as cmod

# Create your models here.
class FomoUser(AbstractUser):
    ## See Django documentation for attributes inherited from AbstractUser
    birthday = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length = 20)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50)
    zipcode = models.CharField(max_length = 50)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def _get_full_address(self):
        return self.address + ' ' + self.city + ', ' + self.state + ' ' + self.zipcode
    full_address = property(_get_full_address)


    def verify_address(self):
        return geo(self.full_address)
