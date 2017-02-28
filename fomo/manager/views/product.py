from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.decorators import permission_required, login_required
from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from formlib.form import FormMixIn
from catalog import models as cmod

@view_function
@login_required
@permission_required('catalog.change_product', raise_exception=True)
def process_request(request):

    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/manager/products')

    # process the form
    form = EditProductForm(request, product=product, initial={
        'id': product.id,
        'name': product,
        'category': product.category,
        'brand': product.brand,
        'price': product.price,
        'serial_number': getattr(product, 'serial_number', 0),
        'quantity': getattr(product, 'quantity', 0),
        'reorder_point': getattr(product, 'reorder_point', 0),
        'reorder_quantity': getattr(product, 'reorder_quantity', 0),
    })

    if form.is_valid():
        form.commit(product)
        return HttpResponseRedirect('/manager/products/')

    context = {
        'product' : product,
        'form': form,
        'title': 'Edit Product',
    }
    print(form)
    return dmp_render(request, 'product.html', context)



class EditProductForm(FormMixIn, forms.Form):

    def init(self, product):

        self.fields['name'] = forms.CharField(label='Product Name', max_length=100)
        self.fields['category'] = forms.ModelChoiceField(label="Category",
            queryset=cmod.Category.objects.order_by('name').all())
        self.fields['brand'] = forms.CharField(label='Brand', max_length=100)
        self.fields['price'] = forms.DecimalField(label='Price')
        if hasattr(product, 'serial_number'):
            self.fields['serial_number'] = forms.CharField(label='Serial Number')
        if hasattr(product, 'quantity'):
            self.fields['quantity'] = forms.IntegerField(label='Quantity')
        if hasattr(product, 'reorder_point'):
            self.fields['reorder_point'] = forms.IntegerField(label='Reorder Point')
        if hasattr(product, 'reorder_quantity'):
            self.fields['reorder_quantity'] = forms.IntegerField(label='Reorder Quantity')

    def commit(self, product):
        product.name = self.cleaned_data.get('name')
        product.category = self.cleaned_data.get('category')
        product.brand = self.cleaned_data.get('brand')
        product.price = self.cleaned_data.get('price')
        if hasattr(product, 'serial_number'):
            product.serial_number = self.cleaned_data.get('serial_number')
        if hasattr(product, 'quantity'):
            product.quantity = self.cleaned_data.get('quantity')
        if hasattr(product, 'reorder_point'):
            product.reorder_point = self.cleaned_data.get('reorder_point')
        if hasattr(product, 'reorder_quantity'):
            product.reorder_quantity = self.cleaned_data.get('reorder_quantity')
        product.save()


###################################################
## Deleting of products

@view_function
@login_required
@permission_required('catalog.delete_product', raise_exception=True)
def delete(request):
    try:
        product = cmod.Product.objects.get(id=request.urlparams[0])
    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/manager/products')

    product.delete()
    return HttpResponseRedirect('/manager/products')


###################################################
## Creating products

@view_function
@login_required
@permission_required('catalog.add_product', raise_exception=True)
def create(request):
        product = cmod.Product()

        # process the form
        form = CreateProductForm(request, product=product)

        if form.is_valid():
            print('>>> form is valid')
            form.commit(product)
            return HttpResponseRedirect('/manager/products/')

        context = {
            'product' : product,
            'form': form,
            'title': 'Create a New Product',
        }

        return dmp_render(request, 'product.html', context)


class CreateProductForm(FormMixIn, forms.Form):

    def init(self, product):

        PRODUCT_TYPE_CHOICES = [
            ['bulk_product', 'BulkProduct'],
            ['unique_product', 'UniqueProduct'],
            ['rental_product', 'RentalProduct']
        ]

        self.fields['product_type'] = forms.ChoiceField(label='Product Type', choices=PRODUCT_TYPE_CHOICES)
        self.fields['name'] = forms.CharField(label='Product Name', max_length=100)
        self.fields['category'] = forms.ModelChoiceField(label="Category",
            queryset=cmod.Category.objects.order_by('name').all())
        self.fields['brand'] = forms.CharField(label='Brand', max_length=100)
        self.fields['price'] = forms.DecimalField(label='Price')
        self.fields['serial_number'] = forms.CharField(label='Serial Number', required=False)
        self.fields['quantity'] = forms.IntegerField(label='Quantity', required=False)
        self.fields['reorder_point'] = forms.IntegerField(label='Reorder Point', required=False)
        self.fields['reorder_quantity'] = forms.IntegerField(label='Reorder Quantity', required=False)

    def commit(self, product):
        product_type = self.cleaned_data.get('product_type')

        if product_type == 'bulk_product':
            product = cmod.BulkProduct()
        elif product_type == 'unique_product':
            product = cmod.UniqueProduct()
        else:
            product = cmod.RentalProduct()

        product.name = self.cleaned_data.get('name')
        product.category = self.cleaned_data.get('category')
        product.brand = self.cleaned_data.get('brand')
        product.price = self.cleaned_data.get('price')
        if hasattr(product, 'serial_number'):
            product.serial_number = self.cleaned_data.get('serial_number')
        if hasattr(product, 'quantity'):
            product.quantity = self.cleaned_data.get('quantity')
        if hasattr(product, 'reorder_point'):
            product.reorder_point = self.cleaned_data.get('reorder_point')
        if hasattr(product, 'reorder_quantity'):
            product.reorder_quantity = self.cleaned_data.get('reorder_quantity')
        product.save()
