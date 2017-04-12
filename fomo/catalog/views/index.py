from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from catalog import models as cmod

@view_function
def process_request(request):
    products = cmod.Product.objects.filter(**request.GET.dict())
    brands = products.distinct('brand').values_list('brand', flat=True)
    categories = cmod.Category.objects.all()

    previous_page = request.META.get('HTTP_REFERER')

    context = {
        'categories': categories,
        'products': products,
        'brands': brands,
    }

    return dmp_render(request, 'index.html', context)
