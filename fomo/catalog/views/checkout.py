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

    form = CheckoutForm(request, initial={
        'stripe_token': settings.STRIPE_PRIVATE_KEY,
    })

    if form.is_valid():
        form.commit()

    context = {
        'form': form,
    }
    return dmp_render(request, 'checkout.html', context)

class CheckoutForm(FormMixIn, forms.Form):
    def init(self):
        self.fields['stripe_token'] = forms.CharField(label='public stripe token', max_length=100)
        self.fields['Billing Address'] = forms.CharField(label='Billing Address', max_length=100)

    def clean(self):
        pass

    def commit(self):
        pass
