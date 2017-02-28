$(function() {

  var product_type = $('#id_product_type')

  $('#id_product_type').change(function(event) {
    var value = product_type.val();

    if (value == 'bulk_product'){
      $('#id_serial_number').closest('p').hide();
      $('#id_quantity').closest('p').show();
      $('#id_reorder_point').closest('p').show();
      $('#id_reorder_quantity').closest('p').show();
    }
    else{
      $('#id_serial_number').closest('p').show();
      $('#id_quantity').closest('p').hide();
      $('#id_reorder_point').closest('p').hide();
      $('#id_reorder_quantity').closest('p').hide();
    }
  });

  $('#id_product_type').change();

});
