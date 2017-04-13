$(function() {

  $('#shipping-form-id').ajaxForm({
    target:'#shipping-form-container',
  });//ajaxForm

  $("#load-address-form").click(function(){
    $("#shipping-form-container").load('/catalog/checkout.shipping_form')
  }); //click

  $('#shipping-continue').click(function() {
    $('#accordion').accordion("option", "active", 2)
  });

  $.LiveAddress({
    key: '${ settings.SMARTY_STREET_API_KEY }',
    addresses: [{
      id: 'billing',
      address1: '#id_address',
      locality: '#id_city',
      administrative_area: '#id_state',
      postal_code: '#id_zipcode',
    }]
  });// LiveAddress

});//function
