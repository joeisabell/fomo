import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from catalog import models as cmod

@view_function
@login_required
@permission_required('catalog.change_product', raise_exception=True)
def process_request(request):
    products = cmod.Product.objects.order_by('name').all()
    context = {
        'products' : products,
    }

    return dmp_render(request, 'products.html', context)

@view_function
@login_required
@permission_required('catalog.change_product', raise_exception=True)
def get_quantity(request):
    if request.is_ajax():
        product = cmod.Product.objects.get(id=request.urlparams[0])
        quantity = product.quantity
        return HttpResponse(quantity)
    else:
        raise Http404

@view_function
@login_required
@permission_required('catalog.change_product', raise_exception=True)
def product_info(request):
    if request.is_ajax():
        product = cmod.Product.objects.get(id=request.urlparams[0])
        attributes = [product.name, product.brand, product.category.name, ]
        data = json.dumps(attributes)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
