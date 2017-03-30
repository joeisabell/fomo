$(function() {

  var form = $('#payment_form_container > form')
  console.log(form)

  var handler = StripeCheckout.configure({
    key: '${ settings.STRIPE_PUBLIC_KEY }',
    image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
    locale: 'auto',
    token : function(token){
      $('#id_stripe_token').val(token.id);
      form.submit();
    }
  });
  console.log(handler)

  form.submit(function(e) {
    if ($('#id_stripe_token').val()) {
      // Open checkout with further options
      handler.open({
        name: 'FOMO Music Store',
        description: '2 Widgets',
        amount: 2000
      });
    e.preventDefault();
    }
  });

});
