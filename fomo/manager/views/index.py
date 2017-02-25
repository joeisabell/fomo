from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required, permission_required
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from account import models as amod

@view_function
@login_required
@permission_required('account.change_fomouser', raise_exception=True)
def process_request(request):

    return dmp_render(request, 'index.html')
