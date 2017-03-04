import os
from datetime import datetime
from decimal import Decimal

# initialize django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()

from django.core import management
from django.db import connection
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

from catalog import models as cmod
from account import models as amod

# drop and recreate database tables
with connection.cursor() as cursor:
    cursor.execute("DROP SCHEMA public CASCADE")
    cursor.execute("CREATE SCHEMA public")
    cursor.execute("GRANT ALL ON SCHEMA public TO postgres")
    cursor.execute("GRANT ALL ON SCHEMA public TO public")

# migrate
management.call_command('makemigrations')
management.call_command('migrate')

# add groups
for data in (
        ('Managers', Permission.objects.all()),
        ('Customers', ()),
    ):
    group = Group()
    group.name = data[0]
    group.save()
    group.permissions.set(data[1])

# add users
for data in (
        ('Joe', 'Isabell', 'joeisabell0@gmail.com', 'isabell7', 'Utslcw2014', True, True, '465 N 300 W Apt 29', 'Provo', 'UT', '84601', '479-802-9621', ['Managers', 'Customers']),
        ('Margo', 'Isabell', 'margobrockbank5@gmail.com', 'misabell', 'mypass', False, False, '465 N 300 W Apt 29', 'Provo', 'UT', '84601', '479-802-9621', ['Customers',]),
        ('Jim', 'Fife', 'jamesafife@bearriver.net', 'primeguard68', 'mypass', False, False, '12695 Strawberry Ridge Road', 'Bentonville', 'AR', '72712', '479-898-3344', ['Customers',]),
        ('Jill', 'River', 'jill@bearriver.net', 'jackrabit', 'mypass', False, False, '12695 Strawberry Ridge Road', 'Bentonville', 'AR', '72712', '479-898-3344', ['Customers',]),
    ):
    user = amod.FomoUser()
    user.first_name = data[0]
    user.last_name = data[1]
    user.email = data[2]
    user.username = data[3]
    user.set_password(data[4])
    user.is_staff = data[5]
    user.is_active = data[6]
    user.address = data[7]
    user.city = data[8]
    user.state = data[9]
    user.zipcode = data[10]
    user.phone = data[11]
    user.last_login = datetime.now()
    user.date_joined = datetime.now()
    user.save()
    for group_name in data[12]:
        group = Group.objects.get(name__exact=group_name)
        user.groups.add(group)

# add categories
for data in (
        ('Brass Instruments', 'brass'),
        ('String Instruments', 'string'),
        ('Wind Instruments', 'wind'),
    ):
    cat = cmod.Category()
    cat.name = data[0]
    cat.codename = data[1]
    cat.save()

## add products
# add bulk products
for data in (
        ('Trumpet Mouthpiece', 'brass', 'Galaxy', Decimal('49.99'), 20, 5, 10),
        ('E String', 'string', 'E-Tude', Decimal('9.99'), 20, 5, 10),
    ):
    bulk_product = cmod.BulkProduct()
    bulk_product.name = data[0]
    bulk_product.category = cmod.Category.objects.get(codename__exact=data[1])
    bulk_product.brand = data[2]
    bulk_product.price = data[3]
    bulk_product.quantity = data[4]
    bulk_product.reorder_point = data[5]
    bulk_product.reorder_quantity = data[6]
    bulk_product.save()

# add unique products
for data in (
        ('Trumpet', 'brass', 'Galaxy', Decimal('450.00'), '908839'),
        ('Tuba', 'brass', 'E-Tude', Decimal('999.99'), '909839'),
        ('French Horn', 'brass', 'Galaxy', Decimal('649.99'), '909787'),
    ):
    unique_product = cmod.UniqueProduct()
    unique_product.name = data[0]
    unique_product.category = cmod.Category.objects.get(codename__exact=data[1])
    unique_product.brand = data[2]
    unique_product.price = data[3]
    unique_product.serial_number = data[4]
    unique_product.save()

# add rental products
for data in (
        ('Clarinet', 'wind', 'Windy', Decimal('499.99'), '900839'),
        ('Violin', 'string', 'E-Tude', Decimal('1499.99'), '809839'),
        ('Electric Guitar', 'string', 'Fender', Decimal('575.99'), '909187'),
    ):
    rental_product = cmod.RentalProduct()
    rental_product.name = data[0]
    rental_product.category = cmod.Category.objects.get(codename__exact=data[1])
    rental_product.brand = data[2]
    rental_product.price = data[3]
    rental_product.serial_number = data[4]
    rental_product.save()
