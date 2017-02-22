from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from account import models as amod

@view_function
def process_request(request):
    users = amod.FomoUser.objects.order_by('last_name').all()

    context = {
        'users' : users,
    }

    return dmp_render(request, 'users.html', context)
