import json

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
    users = amod.FomoUser.objects.order_by('last_name').all()

    context = {
        'users' : users,
    }
    return dmp_render(request, 'users.html', context)

@view_function
@login_required
@permission_required('account.change_fomouser', raise_exception=True)
def user_info(request):
    if request.is_ajax():
        user = amod.FomoUser.objects.get(id=request.urlparams[0])
        attributes = [user.get_full_name(), user.username, user.email, ]
        data = json.dumps(attributes)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
