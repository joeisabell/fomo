import os
from django.conf import settings
from django.db import models
from django.core.mail import EmailMultiAlternatives
# Create your models here.

# returns the style text for the email app
def style(tself):
    tname = os.path.split(tself.template.filename)[1].split('.')[0]
    return '/email_app/styles/{}.css'.format(tname)
