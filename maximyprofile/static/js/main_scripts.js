//$( document ).on( 'click', '.details a', function(event) {
//   if (event.target.hasAttribute('href')) {
//       var link = event.target.href + 'ajax/';
//       var link_array = link.split('/');
//       if (link_array[4] == 'category') {
//           $.ajax({
//               url: link,
//               success: function (data) {
//                   $('.details').html(data.result);
//               },
//           });
//
//           event.preventDefault();
//       }
//   }
//});
;(function($) {

  var site_options = {
    'main_color'      : '#71b013',
    'secondary_color' : '#ff9900'
  }

  // Hover effect for the header menu
  $("#categories > ul > li").not("#menu_home").hover(
    function() {
      $(this).find("a:first").stop().animate({
          color: '#ffffff',
          backgroundColor: site_options.secondary_color
        },300
      );
    }
    ,
    function() {
      $(this).find("a:first").stop().animate({
          color: site_options.secondary_color,
          backgroundColor: '#ffffff'
        },300
      );
    }
  );

  if (!$.browser.msie || parseInt($.browser.version, 10) > 8) {
      var onMouseOutOpacity = 1;
      $('div.s_listing > div.s_item').css('opacity', onMouseOutOpacity)
        .hover(
          function () {
            $(this).prevAll().stop().fadeTo('slow', 0.60);
            $(this).nextAll().stop().fadeTo('slow', 0.60);
          },
          function () {
            $(this).prevAll().stop().fadeTo('slow', onMouseOutOpacity);
            $(this).nextAll().stop().fadeTo('slow', onMouseOutOpacity);
          }
      );
  }

  // Hover effect for the shoppica cart
  $("#cart_menu").hover(
    function() {
      $(this).find(".s_grand_total").stop().animate({
          color: '#ffffff',
          backgroundColor: site_options.main_color
        },300
      );
    }
    ,
    function() {
      $(this).find(".s_grand_total").stop().animate({
          color: site_options.main_color,
          backgroundColor: '#ffffff'
        },300
      );
    }
  );
// Hover effect for the shoppica cart
  $("#cart_menu_2").hover(
    function() {
      $(this).find(".s_grand_total").stop().animate({
          color: '#ffffff',
          backgroundColor: site_options.main_color
        },300
      );
    }
    ,
    function() {
      $(this).find(".s_grand_total").stop().animate({
          color: site_options.main_color,
          backgroundColor: '#ffffff'
        },300
      );
    }
  );

  // Animation for the languages and currency dropdown
  $('.s_switcher').hover(function() {
    $(this).find('.s_options').stop(true, true).slideDown('fast');
  },function() {
    $(this).find('.s_options').stop(true, true).slideUp('fast');
  });

  var search_visibility = 0;
  // Animation for the search button
  $("#show_search").bind("click", function(){
    if (search_visibility == 0) {
      $("#search_bar").fadeIn();
      search_visibility = 1;
    } else {
      $("#search_bar").fadeOut();
      search_visibility = 0;
    }
  });
});

;( function($) {

  var site_options = {
    'main_color'      : '#71b013',
    'secondary_color' : '#ff9900'
  }

  // Slider options
  $("#image_intro").slides({
    effect: slideEffect,
    crossfade: true,
    preload: true,
    fadeSpeed: 800,
    slideSpeed: 800,
    next: 's_button_next',
    prev: 's_button_prev',
    play: 5000,
    generatePagination: false
  });

  // Next/Prev buttons hover effect
  $("#intro .s_button_prev, #intro .s_button_next").hover(
    function() {
      $(this).stop().animate({
          backgroundColor: site_options.secondary_color
        },300
      );
    }
    ,
    function() {
      $(this).stop().animate({
          backgroundColor: site_options.main_color
        },300
      );
    }
  );

});

;( function($) {

  var site_options = {
    'main_color'      : '#71b013',
    'secondary_color' : '#ff9900'
  }

  // Slider options
  $("#product_intro_preview").slides({
    slideSpeed: 800,
    next: 's_button_next',
    prev: 's_button_prev',
    play: 5000,
    generatePagination: false,
    animationStart: function() {
      $("#product_intro_info > div:visible").fadeOut('slow');
    },
    animationComplete: function(current) {
      number = $("#product_intro_preview div.slideItem").index($("#product_intro_preview div.slideItem:visible"));
      $("#product_intro_info > div").eq(number).fadeIn();
    }
  });

  // Next/Prev buttons hover effect
  $("#intro .s_button_prev, #intro .s_button_next").hover(
    function() {
      $(this).stop().animate({
          backgroundColor: site_options.secondary_color
        },300
      );
    }
    ,
    function() {
      $(this).stop().animate({
          backgroundColor: site_options.main_color
        },300
      );
    }
  );

});