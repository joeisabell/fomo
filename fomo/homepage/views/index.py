from django.conf import settings
from datetime import datetime

from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):
    context = {
        'now' : datetime.now(),
    }

    return dmp_render(request, 'index.html', context)
