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
        ('Percussion Instruments', 'percussion'),
    ):
    cat = cmod.Category()
    cat.name = data[0]
    cat.codename = data[1]
    cat.save()

# product picture base uri
dir = 'catalog/media/product_images/'

# product description filler
desc =  '''
        Nisi cillum reprehenderit anim esse aute officia Lorem nulla. Cupidatat commodo eiusmod mollit
        dolore esse eu commodo qui nostrud ex fugiat culpa deserunt eu. Non nulla reprehenderit quis minim eiusmod
        culpa qui do anim nisi esse est culpa veniam. Fugiat sint occaecat et minim cillum ut est adipisicing labore
        exercitation ea. Fugiat ut veniam non esse do eu eu quis eu aliquip exercitation fugiat ad eiusmod ea.
        '''
## add products
# add bulk products
for data in (
        ('Trumpet Mouthpiece', 'brass', 'Galaxy', Decimal('49.99'), 20, 5, 10, [
            [ dir + 'trumpet_mouthpiece.jpg', 'jpg', True ],
            [ dir + 'trumpet_mouthpiece_1.jpg', 'jpg', False ],
            [ dir + 'trumpet_mouthpiece_2.jpg', 'jpg', False ],
            [ dir + 'trumpet_mouthpiece_3.jpg', 'jpg', False ],
        ], desc),
        ('Violin String Set', 'string', 'E-Tude', Decimal('9.99'), 20, 5, 10, [
            [ dir + 'violin_string_set.jpg', 'jpg', True ],
            [ dir + 'violin_string_set_1.jpg', 'jpg', False ],
        ], desc),
    ):
    bulk_product = cmod.BulkProduct()
    bulk_product.name = data[0]
    bulk_product.category = cmod.Category.objects.get(codename__exact=data[1])
    bulk_product.brand = data[2]
    bulk_product.price = data[3]
    bulk_product.quantity = data[4]
    bulk_product.reorder_point = data[5]
    bulk_product.reorder_quantity = data[6]
    bulk_product.description = data[8]
    bulk_product.save()
    for img in data[7]:
        product_image = cmod.ProductImage()
        product_image.product = bulk_product
        product_image.subdir = img[0]
        product_image.alttext = bulk_product.name
        product_image.mimetype = img[1]
        product_image.is_primary = img[2]
        product_image.save()

# add unique products
for data in (
        ('Trumpet', 'brass', 'Galaxy', Decimal('450.00'), '908839', [
            [ dir + 'trumpet.jpg', 'jpg', True ],
            [ dir + 'trumpet_1.jpg', 'jpg', False ],
            [ dir + 'trumpet_2.jpg', 'jpg', False ],
            [ dir + 'trumpet_3.jpg', 'jpg', False ],
        ], desc),
        ('Tuba', 'brass', 'E-Tude', Decimal('999.99'), '909839', [
            [ dir + 'tuba.jpg', 'jpg', True ],
            [ dir + 'tuba_1.jpg', 'jpg', False ],
            [ dir + 'tuba_2.jpg', 'jpg', False ],
            [ dir + 'tuba_3.jpg', 'jpg', False ],
        ], desc),
        ('French Horn', 'brass', 'Mendini', Decimal('250.99'), '909787', [
            [ dir + 'french_horn.jpg', 'jpg', True ],
            [ dir + 'french_horn_1.jpg', 'jpg', False ],
            [ dir + 'french_horn_2.jpg', 'jpg', False ],
            [ dir + 'french_horn_3.jpg', 'jpg', False ],
        ], desc),
    ):
    unique_product = cmod.UniqueProduct()
    unique_product.name = data[0]
    unique_product.category = cmod.Category.objects.get(codename__exact=data[1])
    unique_product.brand = data[2]
    unique_product.price = data[3]
    unique_product.serial_number = data[4]
    unique_product.description = data[6]
    unique_product.save()
    for img in data[5]:
        product_image = cmod.ProductImage()
        product_image.product = unique_product
        product_image.subdir = img[0]
        product_image.alttext = unique_product.name
        product_image.mimetype = img[1]
        product_image.is_primary = img[2]
        product_image.save()

# add rental products
for data in (
        ('Clarinet', 'wind', 'Windy', Decimal('499.99'), '900839', [
            [ dir + 'clarinet.jpg', 'jpg', True ],
            [ dir + 'clarinet_1.jpg', 'jpg', False ],
            [ dir + 'clarinet_2.jpg', 'jpg', False ],
            [ dir + 'clarinet_3.jpg', 'jpg', False ],
        ], desc),
        ('Violin', 'string', 'Samsung', Decimal('1499.99'), '809839', [
            [ dir + 'violin.jpg', 'jpg', True ],
            [ dir + 'violin_1.jpg', 'jpg', False ],
            [ dir + 'violin_2.jpg', 'jpg', False ],
            [ dir + 'violin_3.jpg', 'jpg', False ],
        ], desc),
        ('Guitar', 'string', 'Fender', Decimal('575.99'), '909187', [
            [ dir + 'guitar.jpg', 'jpg', True ],
            [ dir + 'guitar_1.jpg', 'jpg', False ],
            [ dir + 'guitar_2.jpg', 'jpg', False ],
            [ dir + 'guitar_3.jpg', 'jpg', False ],
        ], desc),
    ):
    rental_product = cmod.RentalProduct()
    rental_product.name = data[0]
    rental_product.category = cmod.Category.objects.get(codename__exact=data[1])
    rental_product.brand = data[2]
    rental_product.price = data[3]
    rental_product.serial_number = data[4]
    rental_product.description = data[6]
    rental_product.save()
    for img in data[5]:
        product_image = cmod.ProductImage()
        product_image.product = rental_product
        product_image.subdir = img[0]
        product_image.alttext = rental_product.name
        product_image.mimetype = img[1]
        product_image.is_primary = img[2]
        product_image.save()
