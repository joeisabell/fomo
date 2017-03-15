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
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    category = models.ForeignKey('Category')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def default_image(self):
        return self.images.get(is_primary=True)

    def to_json(self):
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
    product = models.ForeignKey(Product, related_name='images')
    subdir = models.TextField()
    alttext = models.TextField(null=True)
    mimetype = models.TextField(null=True)
    is_primary = models.NullBooleanField()
