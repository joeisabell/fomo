$(function() {

  var images = $('#jquery-loadmodal-js-body img');
  var current_image_num = 0;

  function showPic(pnum) {
    images.hide();
    $(images[current_image_num]).show();
  }

  showPic(current_image_num)

  $('#move-right').click(function(){
    current_image_num++;
    if (current_image_num >= images.length) {
      current_image_num = 0;
    }
    showPic();
  });

  $('#move-left').click(function(){
    current_image_num--;
    if (current_image_num <= -1) {
      current_image_num = images.length-1;
    }
    showPic();
  });

});
