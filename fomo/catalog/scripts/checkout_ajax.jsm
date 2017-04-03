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

});//function
