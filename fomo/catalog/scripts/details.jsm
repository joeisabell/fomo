$(function() {

  $('#buy-now-form').ajaxForm({
    target:'#purchase-container',
  });//ajaxForm

  $('#product-image > img').click(function() {
    var pid = $(this).attr('data-pid');
    $.loadmodal({
          url: '/catalog/details.image_modal/' + pid,
          id: 'product-modal',
          title: ' ',
          width: '500px',
          closeButton: true
      })//loadmodal
  });//click

});//function
