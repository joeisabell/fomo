from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login

from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):
    print('>>>> Process Request')
    username = 'isabell7'
    password = 'mypass'
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)

        return HttpResponseRedirect('/account/index')

    # if not authenticated
    return HttpResponseRedirect('/')
