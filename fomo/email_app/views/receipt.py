from email_app.models import FomoEmail

def process_email(template, context):
    email_receipt = FomoEmail(template, context)
    email_receipt.msg.to = [context.get('sale').user.email]
    email_receipt.msg.subject = 'Family Music Order Confirmation'
    email_receipt.msg.text_content = '''
        Thanks for your purchase! View this receipt online here.
        https://familymusic.us/catalog/receipt/{}
    '''.format(context.get('sale').id)

    email_receipt.send()
