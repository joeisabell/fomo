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

management.call_command('makemigrations')
management.call_command('migrate')

# add groups
#g1 = Group()
#g1.name = 'Supers'
#g1.save()

#for p in Permissions.objects.all()
#    g1.permissions.add(p)

#g2 = Group()
#g2.name = 'Salesperson'
#g2.save()

#g2.persmissions.add(Permission.objects.get(codename=('add_fomouser')))
#g2.persmissions.add(Permission.objects.get(codename=('change_fomouser')))
#g2.persmissions.add(Permission.objects.get(codename=('delete_fomouser')))

# add users
u1 = amod.FomoUser()
u1.set_password("Utslcw2014")
u1.last_login = datetime.now()
u1.is_superuser = True
u1.username = "isabell7"
u1.first_name = "Joe"
u1.last_name = "Isabell"
u1.email = "joeisabell0@gmail.com"
#u1.groups.add(g1)
u1.is_staff = True
u1.is_admin = True
u1.is_active = True
u1.date_joined = datetime.now()
u1.address = "465 N 300 W Apt 29"
u1.city = "Provo"
u1.state = "UT"
u1.zip_code = "84601"
u1.phone = "479-802-9621"
u1.save()

u2 = amod.FomoUser()
u2.set_password("mypass")
u2.last_login = datetime.now()
u2.is_superuser = True
u2.username = "misabell"
u2.first_name = "Margo"
u2.last_name = "Isabell"
u2.email = "margobrockbank5@gmail.com"
u2.is_staff = True
u2.is_active = True
u2.date_joined = datetime.now()
u2.address = "465 N 300 W Apt 29"
u2.city = "Provo"
u2.state = "UT"
u2.zip_code = "84601"
u2.phone = "479-802-9621"
u2.save()

u3 = amod.FomoUser()
u3.set_password("mypass")
u3.last_login = datetime.now()
u3.is_superuser = True
u3.username = "primeguard68"
u3.first_name = "Jim"
u3.last_name = "Fife"
u3.email = "jamesafife@bearriver.net"
u3.is_staff = True
u3.is_active = True
u3.date_joined = datetime.now()
u3.address = "12695 Strawberry Ridge Road"
u3.city = "Bentonville"
u3.state = "AR"
u3.zip_code = "72712"
u3.phone = "479-898-3344"
u3.save()

u4 = amod.FomoUser()
u4.set_password("mypass")
u4.last_login = datetime.now()
u4.is_superuser = True
u4.username = "jackrabit"
u4.first_name = "Jack"
u4.last_name = "Rabbit"
u4.email = "jill@bearriver.net"
u4.is_staff = True
u4.is_active = True
u4.date_joined = datetime.now()
u4.address = "12695 Strawberry Ridge Road"
u4.city = "Bentonville"
u4.state = "AR"
u4.zip_code = "72712"
u4.phone = "479-898-3344"
u4.save()

# add categories
cat1 = cmod.Category()
cat1.code = 'brass'
cat1.name = 'Brass Instruments'
cat1.save()

# add products
bp1 = cmod.BulkProduct()
bp1.category = cat1
bp1.name = 'Kazoo'
bp1.brand = 'ToysRUs'
bp1.price = Decimal('90.50')
bp1.quantity = 20
bp1.reorder_point = 5
bp1.reorder_quantity = 10
