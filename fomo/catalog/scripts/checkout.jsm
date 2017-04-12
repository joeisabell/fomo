$(function() {

  $( "#accordion" ).accordion({
    heightStyle: "content",
  });

  $('#summary-continue').click(function() {
    $('#accordion').accordion("option", "active", 1)
  });

  $('#shipping-continue').click(function() {
    $('#accordion').accordion("option", "active", 2)
  });

  $("#load-address-form").click(function(){
    $("#shipping-form-container").load('/catalog/checkout.shipping_form')
  }); //click

  var form = $('#payment_form_container > form')

  var handler = StripeCheckout.configure({
    key: '${ settings.STRIPE_PUBLIC_KEY }',
    image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
    locale: 'auto',
    token : function(token){
      $('#id_stripe_token').val(token.id);
      form.submit();
    }
  });

  form.submit(function(e) {
    if ($('#id_stripe_token').val()=='') {
      // Open checkout with further options
      handler.open({
        name: 'FOMO Music Store',
        description: "Number of items: " + ${ request.user.shopping_cart.item_count()},
        amount: ${ request.user.shopping_cart.total * 100 }
      });
    e.preventDefault();
    }
  });

  window.addEventListener('popstate', function() {
      handler.close();
  });

});
