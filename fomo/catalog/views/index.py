from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from catalog import models as cmod

@view_function
def process_request(request):
    try:
        if request.GET.get('categoryid') is not None:
            category = cmod.Category.objects.get(id=request.GET.get('categoryid'))
            products = cmod.Product.objects.filter(category=category)
        else:
            products = cmod.Product.objects.all()
    except:
        products = cmod.Product.objects.all()

    categories = cmod.Category.objects.all()

    previous_page = request.META.get('HTTP_REFERER')

    context = {
        'categories': categories,
        'products': products,
    }

    return dmp_render(request, 'index.html', context)
