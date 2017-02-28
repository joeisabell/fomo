$(function() {

    $('.delete_button').click(function() {
        var uid = $(this).attr('data-uid');
        var modal = $('#myModal').modal()

        $.ajax({
            url: '/manager/users.user_info/' + uid,
            success: function(data) {
              $('.modal-body').html(
                '<h3>'+data[0]+'</h3>' +
                '<h4>Username: '+data[1]+'</h4>' +
                '<h4>Email: '+data[2]+'</h4>'
              );
            }
        })

        $('.confirm_delete').click(function() {
            console.log('confirm and execute' + uid)
            window.location.href = '/manager/user.delete/' + uid
        });

    });
});
