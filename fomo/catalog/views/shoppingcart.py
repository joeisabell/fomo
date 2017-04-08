from django.conf import settings
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string
import stripe

from formlib.form import FormMixIn
from account import models as amod
from catalog.models import ShoppingCart

@view_function
@login_required
def process_request(request):

    context = {
        'cart': request.user.shopping_cart,
    }
    return dmp_render(request, 'shoppingcart.html', context)

@view_function
@login_required
def remove_item(request):
    cart = request.user.shopping_cart
    try:
        cart_item = cart.active_items.get(id=request.urlparams[0])
    except ShoppingCart.DoesNotExist:
        pass
    cart.remove_item(cart_item)
    return HttpResponseRedirect('/catalog/shoppingcart')
