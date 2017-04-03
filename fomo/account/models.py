from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
import googlemaps

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
        return FomoUser.geocode_address(self.full_address)

    @staticmethod
    def geocode_address(address):
        gmaps = googlemaps.Client(key=settings.GOOGLE_SERVER_KEY)
        g_result = gmaps.geocode(address)

        # flatten out address_components of geocode response to be more usable
        g_components = {}
        for component in g_result[0].get('address_components'):
            key = component.get('types')[0]
            value = component.get('short_name')
            g_components[key] = value

        # build address from components and add apt number to address if exists
        g_address = g_components.get('street_number') + ' ' + g_components.get('route')
        if g_components.get('subpremise'):
            g_address += ' #' + g_components.get('subpremise')

        return {
            'full_address': g_address + ' ' + g_components.get('locality') + ', ' + g_components.get('administrative_area_level_1') + ' ' + g_components.get('postal_code'),
            'address': g_address,
            'city': g_components.get('locality'),
            'state': g_components.get('administrative_area_level_1'),
            'zipcode': g_components.get('postal_code'),
        }
