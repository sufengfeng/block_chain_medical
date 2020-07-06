/*========================================================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Project:        Codexo HTML5 Business Template 
Version:        1.0
Last change:    17/03/2020
Primary use:    Business Template 
Author:         Theme_XD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

========================================================================*/
$(function () {
	"use strict";
	$('body').scrollspy({
		target: '#nav-part'
	});
	// for navbar background color when scrolling
	$(window).scroll(function () {
		var $scrolling = $(this).scrollTop();
		var bc2top = $("#back-top-btn");
		if ($scrolling > 150) {
			bc2top.fadeIn(2000);
		} else {
			bc2top.fadeOut(2000);
		}
	});

	//Preloader js
	$('#musa-loader').delay(1500).fadeOut(500);




	// this is for back to top js
	var bc2top = $('#back-top-btn');
	bc2top.on('click', function () {
		html_body.animate({
			scrollTop: 0
		}, 1500);
	});


	//==================Animated Scroll Start==================

    var html_body = $('html, body');
    $('nav a').on('click', function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                html_body.animate({
                    scrollTop: target.offset().top - 50
                }, 1500);
                return false;
            }
        }
    });

	$('.leader_slick').slick({
		infinite: true,
		slidesToShow: 4,
		slidesToScroll: 1,
		autoplay: false,
		arrows: false,
		autoplaySpeed: 2000,
		responsive: [

			{
				breakpoint: 1100,
				settings: {
					centerPadding: '10px',
					slidesToShow: 4,
					slidesToScroll: 1,
					infinite: true

				}
    },
			{
				breakpoint: 767,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 1,
					infinite: true
				}
    },

			{
				breakpoint: 575,
				settings: {

					infinite: true,
					slidesToShow: 1,
					slidesToScroll: 1

				}
    }
  ]
	});

	$('.testimonial_slick').slick({
		infinite: true,
		slidesToShow: 1,
		slidesToScroll: 1,
		autoplay: true,
		arrows: true,
		prevArrow: '<i class="fa fa-long-arrow-right slidNext"></i>',
		nextArrow: '<i class="fa fa-long-arrow-left slidprev"></i>',
		dots: false,
		autoplaySpeed: 1500,
		responsive: [
			{
				breakpoint: 1024,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1,
					infinite: true

				}
    },
			{
				breakpoint: 768,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
    },
			{
				breakpoint: 680,
				settings: {
					arrows: false,
					slidesToShow: 1,
					slidesToScroll: 1

				}
    }
  ]
	});

	$('.people_slick').slick({
		infinite: true,
		slidesToShow: 3,
		slidesToScroll: 1,
		autoplay: true,
		arrows: false,
		dots: true,
		autoplaySpeed: 1500,
		responsive: [
			{
				breakpoint: 1024,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1,
					infinite: true

				}
    },
			{
				breakpoint: 768,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
    },
			{
				breakpoint: 680,
				settings: {
					arrows: false,
					slidesToShow: 1,
					slidesToScroll: 1

				}
    }
  ]
	});

	$('.picing-slick').slick({
		infinite: false,
		centerPadding: '0px',
		centerMode: true,
		focusOnSelect: true,
		slidesToShow: 3,
		slidesToScroll: 1,
		autoplay: false,
		arrows: false,
		autoplaySpeed: 2500,
		responsive: [

			{
				breakpoint: 1100,
				settings: {
					centerPadding: '10px',
					slidesToShow: 3,
					slidesToScroll: 1,
					infinite: true

				}
    },
			{
				breakpoint: 990,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 1,
					infinite: true
				}
    },

			{
				breakpoint: 767,
				settings: {
					infinite: true,
					slidesToShow: 1,
					slidesToScroll: 1

				}
    }
  ]
	});

	// Isotop 

	var $grid = $('.grid').isotope({
		itemSelector: '.element-item',
		layoutMode: 'fitRows',
		getSortData: {
			name: '.name',
			symbol: '.symbol',
			number: '.number parseInt',
			category: '[data-category]',
			weight: function (itemElem) {
				var weight = $(itemElem).find('.weight').text();
				return parseFloat(weight.replace(/[\(\)]/g, ''));
			}
		}
	});

	// filter functions

	var filterFns = {
		// show if number is greater than 50
		numberGreaterThan50: function () {
			var number = $(this).find('.number').text();
			return parseInt(number, 10) > 50;
		},
		// show if name ends with -ium
		ium: function () {
			var name = $(this).find('.name').text();
			return name.match(/ium$/);
		}
	};

	$(".test").click(function () {
		$('html,body').animate({
				scrollTop: $("#pricing-details").offset().top
			},
			1400);
	});
	
	$(".text-2").click(function () {
		$('html,body').animate({
				scrollTop: $("#premium").offset().top
			},
			1400);
	});

	$("a.button-banner").click(function () {
		$('html,body').animate({
				scrollTop: $("#feature").offset().top
			},
			1200);
	});


	//Progress bar 
	$(function () {
		$(".moreBox").slice(0, 3).show();
		$("#loadMore").on('click', function (e) {
			e.preventDefault();
			$(".moreBox:hidden").slice(0, 3).slideDown();
			if ($(".moreBox:hidden").length == 0) {
				$("#load").fadeOut('slow');
			}
		});
	});



	// youtube video js start here
	jQuery("a.bla-1").YouTubePopUp({
		autoplay: 0
	}); // Disable autoplay


	// for Project section filter button click
	$('#filters').on('click', 'button', function () {
		var filterValue = $(this).attr('data-filter');
		// use filterFn if matches value
		filterValue = filterFns[filterValue] || filterValue;
		$grid.isotope({
			filter: filterValue
		});
	});
    // change is-checked class on buttons
	$('.button-group').each(function (i, buttonGroup) {
		var $buttonGroup = $(buttonGroup);
		$buttonGroup.on('click', 'button', function () {
			$buttonGroup.find('.is-checked').removeClass('is-checked');
			$(this).addClass('is-checked');
		});
	});

});