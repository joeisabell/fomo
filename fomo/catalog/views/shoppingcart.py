from django.conf import settings
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string
import stripe

from formlib.form import FormMixIn
from account import models as amod

@view_function
def process_request(request):
    try:
        user = amod.FomoUser.objects.get(id=request.user.id)
    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/account/login')

    context = {
        'cart': user.shopping_cart,
    }
    return dmp_render(request, 'shoppingcart.html', context)
