from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseRedirect
from django_mako_plus import view_function

from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):
    print(request.GET.get('user_name'))
    print(request.GET.get('user_mail'))
    print(request.GET.get('user_message'))

    return dmp_render(request, 'contact.html',{})
