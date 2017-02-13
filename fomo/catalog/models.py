from django.db import models
from polymorphic.models import PolymorphicModel

# Create your models here.

class Category(models.Model):
    #id
    code = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

class Product(PolymorphicModel):
    #id
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    category = models.ForeignKey('Category')

class BulkProduct(Product):
    #id
    quantity = models.IntegerField(default=0)
    reorder_point = models.IntegerField(default=0)
    reorder_quantity = models.IntegerField(default=0)
    #vendor

class UniqueProduct(Product):
    #id
    serial_number = models.TextField(blank=True, null=True)

class RentalProduct(Product):
    #id
    serial_number = models.TextField(blank=True, null=True)
