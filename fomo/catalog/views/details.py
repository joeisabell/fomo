from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from catalog import models as cmod

@view_function
def process_request(request):

    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/catalog/index')

    # add product to last 5 products list
    if product.id in request.last5:
        request.last5.remove(product.id)
        request.last5products.remove(product)

    request.last5.insert(0, product.id)
    request.last5products.insert(0, product)

    previous_page = request.META.get('HTTP_REFERER')
    
    context = {
        'product': product,
        'previous_page': previous_page,
    }
    return dmp_render(request, 'details.html', context)

@view_function
def image_modal(request):

    if request.is_ajax():
        product = cmod.Product.objects.get(id=request.urlparams[0])
        images = cmod.ProductImage.objects.filter(product=product)
    else:
        raise Http404

    context = {
        'product': product,
        'product_images': images,
    }
    return dmp_render(request, 'image_modal.html', context)
