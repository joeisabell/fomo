from decimal import Decimal
from datetime import datetime

from django.db import models
from django.db.models import Sum
from polymorphic.models import PolymorphicModel

from account.models import FomoUser

#####################################################################
## Products

class Category(models.Model):
    name = models.TextField(blank=True, null=True)
    codename = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(PolymorphicModel):
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    category = models.ForeignKey('Category')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def default_image(self):
        return self.images.get(is_primary=True)
    image = property(default_image)

    def check_qty(self):
        if hasattr(self, 'quantity'):
            qty = self.quantity
        else:
            qty = 1 if self.sold is False else 0
        return qty

    def to_json(self):
        '''
        Method used primarily for returning a more user friendly
        JSON response to api requests.
        '''
        json = {}
        for field in self._meta.get_fields():
            if field.related_model == None:
                attr = str(field).split('.')[2]
                val = getattr(self, attr, ' ')
                json[attr] = str(val)

        json['category'] = {
            'name': self.category.name,
            'codename': self.category.codename,
        }

        product_images = {}
        for image in self.images.all():
            product_images[image.id] = {
                'uri': image.subdir,
                'alttext': image.alttext,
                'primary': image.is_primary,
            }

        json['product_images'] = product_images
        return json

    def _get_details(self):
        # these attributes should be hidden from user
        hidden = [
            'product_images', 'category', 'create_date',
            'modified_date', 'quantity', 'id', 'reorder_point', 'reorder_quantity']
        # product details dictionary used for populating the product information table
        product_details = {k:v for (k,v) in self.to_json().items() if k not in hidden}
        product_details['category'] = self.category.name
        product_details['price'] = '$' + str(self.price)
        return product_details
    details = property(_get_details)

    def __str__(self):
        return self.name

class BulkProduct(Product):
    quantity = models.IntegerField(default=0, null=True)
    reorder_point = models.IntegerField(default=0, null=True)
    reorder_quantity = models.IntegerField(default=0, null=True)

class UniqueProduct(Product):
    serial_number = models.TextField(blank=True, null=True)
    sold = models.BooleanField(default=False)

class RentalProduct(Product):
    serial_number = models.TextField(blank=True, null=True)
    sold = models.BooleanField(default=False)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images')
    subdir = models.TextField()
    alttext = models.TextField(null=True)
    mimetype = models.TextField(null=True)
    is_primary = models.NullBooleanField()


######################################################################
## Shopping

class ViewHistory(models.Model):
    user = models.ForeignKey(FomoUser, related_name='view_history')
    product = models.ForeignKey(Product, related_name='view_history')
    view_date = models.DateTimeField(auto_now_add=True)
    added_to_cart = models.BooleanField(default=False)

    @staticmethod
    def add(user, product):
        item_view = ViewHistory()
        item_view.user = FomoUser.objects.get(id=user.id)
        item_view.product = product
        item_view.save()
        return item_view

    @staticmethod
    def last_five(user):
        products = []
        for view in user.view_history.order_by('view_date').reverse():
            if view.product not in products:
                products.append(view.product)
        return products[:5]

class ShoppingCart(models.Model):
    user = models.OneToOneField(FomoUser, related_name='shopping_cart')

    def active_items(self):
        return self.items.filter(purchase_date=None, remove_date=None)

    def add_item(self, product, qty=1):

        if product.id not in self.items.values_list('product__id', flat=True):
            shopping_cart_item = ShoppingCartItem(shopping_cart=self, product=product, quantity=qty)
            shopping_cart_item.save()
            print('add')
        else:
            shopping_cart_item = self.items.get(product=product)
            if hasattr(product, 'quantity'):
                shopping_cart_item.quantity = shopping_cart_item.quantity + qty
                shopping_cart_item.save()

        return shopping_cart_item

    def remove_item(self, shopping_cart_item):
        shopping_cart_item = shopping_cart_item
        shopping_cart_item.remove_date = datetime.now()
        shopping_cart_item.save()

    def clear_cart(self):
        for item in self.items.all():
            print(item)

    def _calc_subtotal(self):
        subtotal = 0
        for item in self.active_items():
            subtotal += item.subtotal
        return subtotal
    subtotal = property(_calc_subtotal)

    def _calc_tax(self):
        return self.subtotal * Decimal('.0725')
    taxes = property(_calc_tax)

    def _calc_shipping(self):
        return 10
    shipping = property(_calc_shipping)

    def _calc_total(self):
        return self.subtotal + self.taxes + self.shipping
    total = property(_calc_total)

class ShoppingCartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, related_name='items')
    product = models.ForeignKey(Product)
    add_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    qty_updated_date = models.DateTimeField(auto_now=True)
    purchase_date = models.DateTimeField(null=True)
    remove_date = models.DateTimeField(null=True)

    def _calc_subtotal(self):
        subtotal = self.product.price * self.quantity
        return subtotal
    subtotal = property(_calc_subtotal)




######################################################################
## Checkout
