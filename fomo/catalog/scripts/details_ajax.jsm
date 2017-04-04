$(function() {

  $('#buy-now-form').ajaxForm({
    target:'#purchase-container',
  });//ajaxForm

  var badge = $('#badge-notify')
  badge.html("${ request.user.shopping_cart.item_count()}");
  if(badge.html() > 0) {
    badge.show()
  }

  var alertClass = ${"'alert-success'" if form.inv_status[0] else "'alert-danger'"}
  $('#form-response').addClass(alertClass)

  $('#alert-message').html('${form.response_message}');

  var alert = $('#form-response')
  alert.show()
  alert.removeClass('hidden').delay(4000).fadeOut(900);

});//function
