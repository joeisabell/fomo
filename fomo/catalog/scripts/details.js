$(function() {

  // var images = $('#jquery-loadmodal-js-body img');
  // var current_image_num = 0;
  //
  // function showPic(pnum) {
  //   images.hide();
  //   
  //   var current = $(images[current_image_num]);
  //   current.show()
  // }
  //
  // showPic(current_image_num)
  //
  // $('#move-right').click(function(){
  //   current_image_num++;
  //   if (current_image_num == images.length) {
  //     current_image_num = 0;
  //   }
  //   showPic();
  //
  // });
  //
  // $('#move-left').click(function(){
  //   current_image_num--;
  //   if (current_image_num == images.length) {
  //     current_image_num = 0;
  //   }
  //   showPic();
  // });

  $('#product-image').click(function() {
      var pid = $(this).attr('data-pid');
      var modal = $('#myModal').modal();

      $.getJSON( '/catalog/details.product_images/' + pid, function( data ) {
          var items = Array.from(data)

          $('#move-right').click(function(){
            console.log(items[2])
            // $('.modal-body').html('<img class="product-images" src="/static/' + items[(nbrOfPics + 1)] +'">')
          });

          $('#move-left').click(function(){
            console.log(next_left(items, $('.modal-body').html()))
            // console.log(items)
            // $('.modal-body').html('<img class="product-images" src="/static/' + items[(nbrOfPics - 1)] +'">')
          });

      });
  });
});
