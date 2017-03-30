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
    # form.data['quantity'] = 1
    if form.is_valid():
        form.commit(product)
        return HttpResponseRedirect('#')

    ViewHistory.add(request.user, product)
    context = {
        'product': product,
        # provide return url to return to the same set of search results
        'previous_page': request.META.get('HTTP_REFERER'),
        'form': form,
    }
    return dmp_render(request, 'details.html', context)

class AddToCartForm(FormMixIn, forms.Form):

    def init(self, product):
        self.product = product
        # form attributes
        self.form_template = 'buy_form.htm'
        self.form_class = 'form-inline'
        self.form_id = 'buy-now-form'
        self.show_qty = True if hasattr(product, 'quantity') else False

        # form fields
        self.fields['quantity'] = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'value':1}))
        # self.data['quantity'] = 1

    def clean_quantity(self):
        print('>>>>>>>>>>>>>>>clean')
        # self.data = self.data.copy()

        qty = self.cleaned_data.get('quantity')
        qty = 1 if qty == 0 else qty
        print(qty)
        if qty >= self.product.check_qty():
            raise forms.ValidationError("We don't have that many in stock :(")
        return qty

    def commit(self, product):
        print('>>>>>>START COMMITT')
        # try:
        #     print('try')
        #     cart_item = self.request.user.shopping_cart.active_items().get(product=product)
        #     cart_item.quantity = cart_item.quantity + self.cleaned_data.get('quantity')
        # except cmod.ShoppingCartItem.DoesNotExist:
        #     print('except')
        cart_item = self.request.user.shopping_cart.add_item(product)
        cart_item.quantity = self.cleaned_data.get('quantity')
        cart_item.save()

        print('>>>>>>>>END COMMITT')


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
