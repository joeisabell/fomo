from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from formlib.form import FormMixIn
from catalog import models as cmod
from catalog.models import ViewHistory

@view_function
def process_request(request):
    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/catalog/index')

    form = AddToCartForm(request, product=product)

    if form.is_valid():
        form.commit(product)

    ViewHistory.add(request.user, product)
    context = {
        'product': product,
        # provide return url to return to the same set of search results
        'previous_page': request.META.get('HTTP_REFERER'),
        'form': form,
    }
    return dmp_render(request, 'details_ajax.html' if request.method == 'POST' else 'details.html' , context)

class AddToCartForm(FormMixIn, forms.Form):

    def init(self, product):
        self.product = product
        self.form_template = 'buy_form.htm'
        self.form_class = 'form-inline'
        self.form_id = 'buy-now-form'
        self.show_qty = False

        if hasattr(product, 'quantity'):
            self.show_qty = True
            self.fields['quantity'] = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'value':1}))

    def clean(self):
        qty = self.cleaned_data.get('quantity')
        qty = 1 if qty == None else qty

        self.inv_status = self.request.user.shopping_cart.check_inv(self.product, qty)
        self.response_message = self.inv_status[1]
        if self.inv_status[0] == False:
            raise forms.ValidationError('')
        return self.cleaned_data

    def commit(self, product):
        if hasattr(product, 'quantity'):
            qty = self.cleaned_data.get('quantity')
        else:
            qty = 1
        cart_item = self.request.user.shopping_cart.add_item(product, qty)
        cart_item.save()

@view_function
def image_modal(request):
    if request.is_ajax():
        product = cmod.Product.objects.get(id=request.urlparams[0])
    else:
        raise Http404

    context = {
        'product': product,
        'product_images': product.images.all(),
    }
    return dmp_render(request, 'image_modal.html', context)
