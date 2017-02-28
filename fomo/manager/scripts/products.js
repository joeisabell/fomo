$(function() {

    $('.update_button').click(function() {
        var pid = $(this).attr('data-pid');
        var quantity = $(this).siblings('.product_quantity')
        quantity.load('/manager/products.get_quantity/' + pid)
    });

    $('.delete_button').click(function() {
        var pid = $(this).attr('data-pid');
        var modal = $('#myModal').modal()

        $.ajax({
            url: '/manager/products.product_info/' + pid,
            success: function(data) {
              $('.modal-body').html(
                '<h3>'+data[0]+'</h3>' +
                '<h4>Brand: '+data[1]+'</h4>' +
                '<h4>Category: '+data[2]+'</h4>'
              );
            }
        })

        $('.confirm_delete').click(function() {
            console.log('confirm and execute' + pid)
            window.location.href = '/manager/product.delete/' + pid
        });

    });
});
