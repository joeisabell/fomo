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

    def _on_hand_qty(self):
        if hasattr(self, 'quantity'):
            qty = self.quantity
        else:
            qty = 1 if self.sold is False else 0
        return qty
    on_hand_qty = property(_on_hand_qty)

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
## Item View History

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
            if len(products) == 5: break
        return products[:5]

######################################################################
## Shopping Cart

class ShoppingCart(models.Model):
    user = models.OneToOneField(FomoUser, related_name='shopping_cart')

    def _active_items(self):
        return self.items.filter(purchase_date=None, remove_date=None)
    active_items = property(_active_items)

    def add_item(self, product, qty=1):
        if product.id not in self.active_items.values_list('product__id', flat=True):
            shopping_cart_item = ShoppingCartItem(shopping_cart=self, product=product, quantity=qty)
            shopping_cart_item.save()
        else:
            shopping_cart_item = self.active_items.get(product=product)
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
            item.remove_date = datetime.now()
            item.save()

    def check_inv(self, product, form_qty):
        # check available inventory and items already in cart
        on_hand_qty = product.on_hand_qty
        try:
            cart_item = self.active_items.get(product=product)
            in_cart_qty = cart_item.quantity
        except ShoppingCartItem.DoesNotExist:
            in_cart_qty = 0
        is_available = form_qty <= on_hand_qty - in_cart_qty
        # based on availability and type of product give the correct
        # notification to be returned to the user
        if is_available:
            alert_message = 'The item has been added to your cart.'
        else:
            if hasattr(product, 'quantity'):
                alert_message = 'Please select a lower number, {} of {} '.format(in_cart_qty, on_hand_qty)
                alert_message += ' items instock are already your cart.'
            else:
                alert_message = 'This item is already in your cart.'
        return (is_available, alert_message)

    def item_count(self):
        count = self.active_items.aggregate(Sum('quantity')).get('quantity__sum')
        return 0 if count == None else count

    def _calc_tax(self):
        tax = self.subtotal * Decimal('.0725')
        return round(tax, 2)
    tax = property(_calc_tax)

    def _calc_shipping(self):
        return Decimal('10')
    shipping_fee = property(_calc_shipping)

    def _calc_subtotal(self):
        subtotal = 0
        for item in self.active_items.all():
            subtotal += item.subtotal
        return subtotal
    subtotal = property(_calc_subtotal)

    def _calc_total(self):
        return self.subtotal + self.tax + self.shipping_fee
    total = property(_calc_total)

class ShoppingCartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, related_name='items')
    product = models.ForeignKey(Product)
    add_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    qty_updated_date = models.DateTimeField(auto_now=True)
    purchase_date = models.DateTimeField(null=True)
    remove_date = models.DateTimeField(null=True)

    def validate_inv(self):
        return self.quantity <= self.product.on_hand_qty

    def _calc_subtotal(self):
        subtotal = self.product.price * self.quantity
        return subtotal
    subtotal = property(_calc_subtotal)

######################################################################
## Checkout

class Sale(models.Model):
    user = models.ForeignKey(FomoUser)
    sale_date = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length = 200, blank=True, null=True)
    city = models.CharField(max_length = 50, blank=True, null=True)
    state = models.CharField(max_length = 50, blank=True, null=True)
    zipcode = models.CharField(max_length = 50, blank=True, null=True)

    def _calc_tax(self):
        return self.line_items.get(sale_item_type='TAX').price
    tax = property(_calc_tax)

    def _calc_shipping_fee(self):
        return self.line_items.get(sale_item_type='SHIPPING').price
    shipping_fee = property(_calc_shipping_fee)

    def _calc_subtotal(self):
        subtotal = 0
        for line_item in self.line_items.filter(sale_item_type='PRODUCT'):
            subtotal += line_item.price
        return subtotal
    subtotal = property(_calc_subtotal)

    def _calc_total(self):
        total = 0
        for line_item in self.line_items.all():
            total += line_item.price
        return total
    total = property(_calc_total)

    @classmethod
    def record(cls, user, shipping_details):
        # create sale object
        sale = cls(user=user, **shipping_details)
        sale.save()
        # add sale line items
        sale._add_cart_items()
        sale._add_tax()
        sale._add_shipping_fee()
        # create payment object
        payment = Payment(sale=sale, charge=sale.total)
        # decrement inventory quantities
        sale._decrement_inv()
        return sale

    def _add_cart_items(self):
        for item in self.user.shopping_cart.active_items.all():
            item.purchase_date = datetime.now()
            item.save()
            line_item = SaleLineItem(sale=self, product=item.product,
                quantity=item.quantity, price=(item.product.price * item.quantity))
            line_item.save()

    def _add_tax(self):
        tax = self.subtotal * Decimal('.0725')
        line_item = SaleLineItem(sale=self, sale_item_type='TAX', quantity=1, price=tax)
        line_item.save()

    def _add_shipping_fee(self):
        line_item = SaleLineItem(sale=self, sale_item_type='SHIPPING', quantity=1, price=self.user.shopping_cart.shipping_fee)
        line_item.save()

    def _decrement_inv(self):
        for item in self.line_items.filter(sale_item_type='PRODUCT'):
            if hasattr(item.product, 'quantity'):
                item.product.quantity -= item.quantity
            else:
                item.product.sold = True
            item.product.save()

class SaleLineItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='line_items')
    sale_item_type = models.CharField(max_length = 50, default='PRODUCT')
    product = models.ForeignKey(Product, null=True)
    quantity = models.IntegerField(default=0, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

class Payment(models.Model):
    sale = models.OneToOneField(Sale)
    stripe_token = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    charge = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
