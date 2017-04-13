from django.conf import settings
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string
import stripe

from fomo.methods import geocode_address as geo
from formlib.form import FormMixIn
from account import models as amod
from catalog.models import Sale
from email_app.views.receipt import process_email

@view_function
@login_required
def process_request(request):
    try:
        user = amod.FomoUser.objects.get(id=request.user.id)
    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/account/login')
    if user.shopping_cart.active_items.count() == 0:
        return HttpResponseRedirect('/catalog/index')

    form = CheckoutForm(request)

    if form.is_valid():
        form.commit()
        return HttpResponseRedirect('/catalog/receipt/{}/'.format(form.sale.id))

    context = {
        'form': form,
    }
    return dmp_render(request, 'checkout.html', context)

class CheckoutForm(FormMixIn, forms.Form):
    def init(self):
        self.form_submit = 'Pay Now with Stripe'
        self.fields['stripe_token'] = forms.CharField(label='private stripe token', required=False, max_length=100, widget=forms.HiddenInput())

    def commit(self):
        user = self.request.user
        shipping_details = self.request.session.get('shipping_address')
        self.sale = Sale.record(user, shipping_details)
        process_email('receipt', { 'sale': self.sale })

@view_function
def shipping_form(request):
    form = ShippingForm(request, initial={
        'address': request.user.address,
        'city': request.user.city,
        'state': request.user.state,
        'zipcode': request.user.zipcode,
        })

    if form.is_valid():
        form.commit()

    return dmp_render(request, 'checkout_ajax.html', {'form': form})

class ShippingForm(FormMixIn, forms.Form):
    def init(self):
        self.fields['address'] = forms.CharField(label='Address', max_length=100)
        self.fields['city'] = forms.CharField(label='City', max_length=100)
        self.fields['state'] = forms.CharField(label='State', max_length=100)
        self.fields['zipcode'] = forms.CharField(label='Zipcode', max_length=100)
        self.form_action = '/catalog/checkout.shipping_form'
        self.form_id = 'shipping-form-id'

    def clean(self):
        address = self.cleaned_data.get('address')
        state = self.cleaned_data.get('state')
        city = self.cleaned_data.get('city')
        zipcode = self.cleaned_data.get('zipcode')
        full_address = address + ' ' + city + ', ' + state + ' ' + zipcode

        # replaced this address geocoding with SmartyStreets JQuery plug-in
        # See checkout.jsm for address validation code as well as https://smartystreets.com/docs for documentation
        # g_result = geo(full_address)
        # self.data = self.data.copy()
        # if full_address != g_result.get('full_address'):
        #     self.data['address'] = g_result.get('address')
        #     self.data['city'] = g_result.get('city')
        #     self.data['zipcode'] = g_result.get('zipcode')
        #     self.data['state'] = g_result.get('state')
        #     raise forms.ValidationError("We verified your address and made some slight changes. Does this address look correct?")

    def commit(self):
        self.request.session['shipping_address'] = {
            'address': self.cleaned_data.get('address'),
            'city': self.cleaned_data.get('city'),
            'state': self.cleaned_data.get('state'),
            'zipcode': self.cleaned_data.get('zipcode'),
        }
