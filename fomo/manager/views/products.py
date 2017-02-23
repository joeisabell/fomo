import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
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

@view_function
def product_info(request):
    if request.is_ajax():
        product = cmod.Product.objects.get(id=request.urlparams[0])
        attributes = [product.name, product.brand, product.category.name, ]
        data = json.dumps(attributes)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
