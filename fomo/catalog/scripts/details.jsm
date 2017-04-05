$(function() {

  $('#buy-now-form').ajaxForm({
    target:'#purchase-container',
  });//ajaxForm

  // $('#buy-now-form > button').click(function(){
  //   $('#form-response').show();
  //   console.log('button pushed')
  // })

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
