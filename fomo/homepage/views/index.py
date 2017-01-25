from django.conf import settings
from django_mako_plus import view_function
from datetime import datetime
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):
    context = {
        'now' : datetime.now(),
    }

    print('>>>>>>>>>>>', context)
    return dmp_render(request, 'index.html', context)
