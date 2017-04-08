from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from catalog.models import Sale

@view_function
def process_request(request):
    try:
        sale = Sale.objects.get(id=request.urlparams[0])
    except Sale.DoesNotExist:
        return HttpResponseRedirect('/catalog/index')

    return dmp_render(request, 'receipt.html', { 'sale': sale })
