from django.db import models
from polymorphic.models import PolymorphicModel

# Create your models here.

class Category(models.Model):
    #id
    name = models.TextField(blank=True, null=True)
    codename = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(PolymorphicModel):
    #id
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    category = models.ForeignKey('Category')

    def primary_image_subdir(self):
        image = ProductImage.objects.get(product=self, is_primary=True)
        return image.subdir

    def __str__(self):
        return self.name

class BulkProduct(Product):
    #id
    quantity = models.IntegerField(default=0, null=True)
    reorder_point = models.IntegerField(default=0, null=True)
    reorder_quantity = models.IntegerField(default=0, null=True)

class UniqueProduct(Product):
    #id
    serial_number = models.TextField(blank=True, null=True)

class RentalProduct(Product):
    #id
    serial_number = models.TextField(blank=True, null=True)

class ProductImage(models.Model):
    product = models.ForeignKey('Product')
    subdir = models.TextField()
    alttext = models.TextField(null=True)
    mimetype = models.TextField(null=True)
    is_primary = models.NullBooleanField()
