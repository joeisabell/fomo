from django.conf import settings
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect

from django_mako_plus import view_function
from .. import dmp_render, dmp_render_to_string
import pynliner

from catalog.models import Sale

def send(request, sale):
    sale = sale
    template = dmp_render_to_string(request, 'receipt.html', {'sale': sale})

    from_email = settings.DEFAULT_FROM_EMAIL
    to = sale.user.email
    subject = 'Family Music Order Confirmation'
    html_content = pynliner.fromString(template)
    text_content = 'Thanks for your purchase! View this receipt online here. https://familymusic.us/catalog/receipt/{}'.format(sale.id)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
