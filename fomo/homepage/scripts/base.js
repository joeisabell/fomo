$(function() {
  $('#modallogin_button').click(function() {
    $.loadmodal('/account/login.modal/')
  });

  if($('#badge-notify').html() == 0) {
    $('#badge-notify').hide()
  }

});
