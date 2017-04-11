import os
from django.conf import settings
from django.db import models
from django.core.mail import EmailMultiAlternatives

from django_mako_plus import get_template_loader
import pynliner
# Create your models here.

# returns the style text for the email app
def style(tself):
    tname = os.path.split(tself.template.filename)[1].split('.')[0]
    return '/email_app/styles/{}.css'.format(tname)

class FomoEmail(object):

    def __init__(self, template, context):
        self.template = '{}.html'.format(template)
        self.context = context
        self.msg = EmailMultiAlternatives()

    def render_html(self):
        tlookup = get_template_loader('email_app', subdir='templates')
        template = tlookup.get_template(self.template)
        template = template.render(context=self.context)
        html_content = pynliner.fromString(template)
        self.msg.attach_alternative(html_content, "text/html")

    def send(self):
        self.render_html()
        self.msg.send()
