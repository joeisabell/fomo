import os

from django.conf import settings
from django.http import HttpResponse

import googlemaps

def letsencrypt(request, acme_data):
    '''
    Method used to return challenge response to ACME CA Server
    '''
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == acme_data:
                challenge = os.path.join(settings.BASE_DIR,'.well-known', 'acme-challenge', file)
    response = open(challenge).read()
    return HttpResponse(response, content_type="text/plain")


def geocode_address(address):
    '''
    Wrapper function for working with Google Geocoding API
    '''
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
