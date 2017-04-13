from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from catalog import models as cmod

@view_function
@login_required
def process_request(request):

    context = {
        'orders': request.user.orders.all(),
    }
    return dmp_render(request, 'orders.html', context)
