from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.postgres.search import SearchVector
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from catalog import models as cmod

@view_function
def process_request(request):
    # if len(request.GET.get('terms')) == 0:
    #     products = ' '
    # else:
    products = cmod.Product.objects.annotate(
            search=SearchVector(
                'name',
                'brand',
                'rentalproduct__serial_number',
                'uniqueproduct__serial_number',
                'category__name',
            ),
        ).filter(search__icontains=request.GET.get('terms'))

    context = {
        'products': products,
    }

    return dmp_render(request, 'search.html', context)
