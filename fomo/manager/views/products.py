from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from catalog import models as cmod

@view_function
def process_request(request):
    products = cmod.Product.objects.order_by('name').all()

    context = {
        'products' : products,
    }

    return dmp_render(request, 'products.html', context)
