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

# # add group
# g1 = Group()
# g1.name = 'Managers'
# g1.save()
# g1.permissions.set(Permission.objects.all())
# g1.save()
#
# g2 = Group()
# g2.name = 'Customers'
# g2.save()

for data in (
        ('Managers', Permission.objects.all()),
        ('Customers', ()),
    ):
    group = Group()
    group.name = data[0]
    group.save()
    group.permissions.set(data[1])
    group.save()

print(Group.objects.all())

for data in (
        ('Joe', 'Isabell', 'joeisabell0@gmail.com', 'isabell7', 'Utslcw2014', True, True, '465 N 300 W Apt 29', 'Provo', 'UT', '84601', '479-802-9621'),
        ('Margo', 'Isabell', 'margobrockbank5@gmail.com', 'misabell', 'mypass', False, False, '465 N 300 W Apt 29', 'Provo', 'UT', '84601', '479-802-9621'),
        ('Jim', 'Fife', 'jamesafife@bearriver.net', 'primeguard68', 'mypass', False, False, '12695 Strawberry Ridge Road', 'Bentonville', 'AR', '72712', '479-898-3344'),
        ('Jill', 'River', 'jill@bearriver.net', 'jackrabit', 'mypass', False, False, '12695 Strawberry Ridge Road', 'Bentonville', 'AR', '72712', '479-898-3344'),
    ):

    user = amod.FomoUser()
    user.first_name = data[0]
    user.last_name = data[1]
    user.email = data[2]
    user.username = data[3]
    user.set_password(data[4])
    user.last_login = datetime.now()
    user.is_staff = data[5]
    user.is_active = data[6]
    user.date_joined = datetime.now()
    user.address = data[7]
    user.city = data[8]
    user.state = data[9]
    user.zip_code = data[10]
    user.phone = data[11]
    user.save()



# u1.groups.add(g1)
# u1.save()


# # add categories
# cat1 = cmod.Category()
# cat1.code = 'brass'
# cat1.name = 'Brass Instruments'
# cat1.save()
#
# cat2 = cmod.Category()
# cat2.code = 'wind'
# cat2.name = 'Wind Instruments'
# cat2.save()
#
# cat3 = cmod.Category()
# cat3.code = 'string'
# cat3.name = 'String Instruments'
# cat3.save()
#
# # add products
# # bulk products
# bp1 = cmod.BulkProduct()
# bp1.category = cat1
# bp1.name = 'Kazoo'
# bp1.brand = 'ToysRUs'
# bp1.price = Decimal('90.50')
# bp1.quantity = 20
# bp1.reorder_point = 5
# bp1.reorder_quantity = 10
# bp1.save()
#
# bp2 = cmod.BulkProduct()
# bp2.category = cat3
# bp2.name = 'E String'
# bp2.brand = 'String City'
# bp2.price = Decimal('10.66')
# bp2.quantity = 40
# bp2.reorder_point = 10
# bp2.reorder_quantity = 20
# bp2.save()
#
# # unique products
# up1 = cmod.UniqueProduct()
# up1.category = cat1
# up1.name = 'Trumpet'
# up1.brand = 'Etude'
# up1.price = Decimal('200.09')
# up1.serial_number = 9458457208
# up1.save()
#
# up2 = cmod.UniqueProduct()
# up2.category = cat1
# up2.name = 'Tuba'
# up2.brand = 'Elite'
# up2.price = Decimal('304.98')
# up2.serial_number = 8474857594
# up2.save()
#
# up3 = cmod.UniqueProduct()
# up3.category = cat1
# up3.name = 'French Horn'
# up3.brand = 'Brass Horns Inc'
# up3.price = Decimal('309.90')
# up3.serial_number = 19384759483
# up3.save()
#
# # rental products
# rp1 = cmod.RentalProduct()
# rp1.category = cat2
# rp1.name = 'Clarinet'
# rp1.brand = 'Elite'
# rp1.price = Decimal('500.98')
# rp1.serial_number = 8374895479
# rp1.save()
#
# rp2 = cmod.RentalProduct()
# rp2.category = cat3
# rp2.name = 'Voilin'
# rp2.brand = 'String City'
# rp2.price = Decimal('1500.98')
# rp2.serial_number = 509588033
# rp2.save()
#
# rp3 = cmod.RentalProduct()
# rp3.category = cat3
# rp3.name = 'Electric Guitar'
# rp3.brand = 'Fender'
# rp3.price = Decimal('576.98')
# rp3.serial_number = 94859584766
# rp3.save()
