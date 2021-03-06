from django.conf import settings
from django.http import JsonResponse, Http404
from django import forms
from django.core import serializers

from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string

from formlib.form import FormMixIn
from catalog import models as cmod

@view_function
def process_request(request):
    form = GetProductForm(request, request.GET.dict())

    if form.is_valid():
        products = cmod.Product.objects.filter(
            name__icontains=form.cleaned_data.get('product_name'),
            category__name__icontains=form.cleaned_data.get('category_name'),
            price__gte=form.cleaned_data.get('min_price'),
            price__lte=form.cleaned_data.get('max_price'),
        )
        products_list = []
        for product in products:
            products_list.append(product.to_json())

            for field in product._meta.get_fields():
                print(field, field.__class__)
                print(field, field.related_model)
                # attr = str(field).split('.')[2]
                # val = getattr(self, attr, ' ')
                # print(val)
                # json[attr] = str(val)

        return JsonResponse(products_list, safe=False)

    return JsonResponse({
        'status': 404,
        'message': 'Invalid query. Please check your url GET parameters',
    })

class GetProductForm(FormMixIn, forms.Form):

    def init(self, product):
        self.fields['product_name'] = forms.CharField(max_length=100, required=False)
        self.fields['category_name'] = forms.CharField(max_length=100, required=False)
        self.fields['min_price'] = forms.DecimalField(required=False)
        self.fields['max_price'] = forms.DecimalField(required=False)

    def clean(self):
        if 'min_price' in self.cleaned_data:
            self.cleaned_data['min_price'] = 0
        if 'max_price' in self.cleaned_data:
            self.cleaned_data['max_price'] = 99999999999

        return self.cleaned_data

    def commit(self):
        pass
