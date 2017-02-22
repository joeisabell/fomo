from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from formlib.form import FormMixIn
from account import models as amod

@view_function
def process_request(request):

    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/manager/products')

    # process the form
    form = EditProductForm(request, product=product, initial={
        'name': product,
        'category': product.category.name,
        'price': product.price,
        'quantity': getattr(product, 'quantity', 0)
    })

    if form.is_valid():
        print('>>> form is valid')
        form.commit(product)
        return HttpResponseRedirect('/app/successurl/')

    context = {
        'product' : product,
        'form': form,
    }

    return dmp_render(request, 'product.html', context)


class EditProductForm(FormMixIn, forms.Form):

    def init(self, product):
        self.fields['name'] = forms.CharField(label='Product Name', max_length=100)
        self.fields['category'] = forms.ModelChoiceField(label="Category",
            queryset=cmod.Category.objects.order_by('name').all())
        self.fields['price'] = forms.DecimalField(label='Price')
        if hasattr(product, 'quantity'):
            self.fields['quantity'] = forms.IntegerField(label='Quantity')

    def commit(self, product):
        product.name = self.form.cleaned_data('name')
        product.category = self.form.cleaned_data.get('category')
        product.price = self.form.cleaned_data.get('price')
        if hasattr(product, 'quantity'):
            product.quantity = self.form.cleaned_data.get('quantity')
        product.save()


###################################################
## Deleting of products

@view_function
def delete(request):
    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/manager/products')

    product.delete()
    return HttpResponseRedirect('/manager/products')
