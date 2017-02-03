from datetime import datetime
from django.core import management
from django.db import connection
import os

# initialize django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()

# drop and recreate database tables
with connection.cursor() as cursor:
    cursor.execute("DROP SCHEMA public CASCADE")
    cursor.execute("CREATE SCHEMA public")
    cursor.execute("GRANT ALL ON SCHEMA public TO postgres")
    cursor.execute("GRANT ALL ON SCHEMA public TO public")

management.call_command('makemigrations')
management.call_command('migrate')

from account.models import FomoUser

u1 = FomoUser()
u1.set_password("mypass")
u1.last_login = datetime.now()
u1.is_superuser = True
u1.username = "isabell7"
u1.first_name = "Joseph"
u1.last_name = "Isabell"
u1.email = "joeisabell0@gmail.com"
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

u2 = FomoUser()
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

u3 = FomoUser()
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

u4 = FomoUser()
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


info = FomoUser.objects.filter(last_name='Isabell')
for hello in info:
		print(hello.id, hello.first_name)
