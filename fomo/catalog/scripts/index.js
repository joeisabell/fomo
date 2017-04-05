$(function(){

  $('.tile-container').hover(
    function(){
      $(this).find('.tile-text').addClass("hover");
      $(this).find('.tile-details').removeClass("hidden");
      console.log('Start_hover');
    },
    function(){
      $(this).find('.tile-text').removeClass("hover");
      $(this).find('.tile-details').addClass("hidden");
      console.log('End_hover');
    });
    
});
