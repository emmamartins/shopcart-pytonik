// some scripts

$(document).ready(function () {

    $('#country_id').on('change', function () {

        var countryID = $(this).val();

        var phonecode = $("option[value=" + $(this).val() + "]", this).attr('phonecode');

        $("#address_phone").val(phonecode);
        $.ajax({
            type: 'POST',
            url: document.location.origin + "/ajax/get_state_by_country",
            data: 'country_id=' + countryID,
            beforeSend: function () {

            },
            success: function (html) {

                

                var JsonResult = JSON.parse(html);
                var getObject = 'States';
                var HTML = '';

                Object.keys(JsonResult).forEach(function (key) {

                    for (var keyr in JsonResult[key]) {

                        if (key == getObject) {
                            HTML += '<option data-tokens="' + JsonResult[key][keyr]["id"] + '" value="' + JsonResult[key][keyr]["id"] + '">' + JsonResult[key][keyr]["name"] + '</option>';

                        }
                    }

                    if (getObject == 'States') {

                        var gethtl = HTML;

                        $("#state_id").html('<option selected value=""> Choose State </option>' + gethtl).trigger('change:update');
                        $("#state_id").trigger('refresh');
                    }
                });


            }
        });
    });

    $('#state_id').on('change', function () {

        var stateID = $(this).val();

        $.ajax({
            type: 'POST',
            url: document.location.origin + "/ajax/get_cities_by_state",
            data: 'state_id=' + stateID,
            beforeSend: function () {

            },
            success: function (html) {


                var JsonResult = JSON.parse(html);
                var getObject = 'Cities';
                var HTML = '';

                Object.keys(JsonResult).forEach(function (key) {

                    for (var keyr in JsonResult[key]) {

                        if (key == getObject) {
                            //console.log(JsonResult[key][keyr]["id"]);

                            HTML += '<option data-tokens="' + JsonResult[key][keyr]["id"] + '" value="' + JsonResult[key][keyr]["id"] + '">' + JsonResult[key][keyr]["name"] + '</option>';

                        }
                    }

                    if (getObject == 'Cities') {

                        var gethtl = HTML;
                        $("#city_id").trigger('refresh');
                        $("#city_id").html('<option selected value=""> Choose City </option>' + gethtl).trigger('change:update');
                        $("#city_id").trigger('refresh');
                    }
                });

            }
        });
    });

});

// jquery ready start
$(document).ready(function() {
	// jQuery code

  // var html_download = '<a href="../../templates.html" class="btn btn-dark rounded-pill" style="font-size:13px; z-index:100; position: fixed; bottom:10px; right:10px;">Download theme</a>';
  //  $('body').prepend(html_download);
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


     ///////////////// fixed menu on scroll for desctop
    if ($(window).width() < 768) {

     	$('.nav-home-aside .title-category').click( function(e){
     		e.preventDefault();
     		$('.menu-category').slideToggle('fast', function() { $('.menu-category .submenu').hide() });
     	});

     	$('.has-submenu a').click( function(e){
     		e.preventDefault();
     		$(this).next().slideToggle('fast');
     	});
 
    } // end if


    // custom checkbox inside card effect
    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
   
    });

	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if


	// offcanvas menu
	$("[data-trigger]").on("click", function(e){
        e.preventDefault();
        e.stopPropagation();
        var offcanvas_id =  $(this).attr('data-trigger');
        $(offcanvas_id).toggleClass("show");
        $('body').toggleClass("offcanvas-active");
        $(".screen-overlay").toggleClass("show");
    }); 

   	// Close menu when pressing ESC
    $(document).on('keydown', function(event) {
        if(event.keyCode === 27) {
           $(".mobile-offcanvas").removeClass("show");
           $("body").removeClass("overlay-active");
        }
    });
    // Close menu by clicking
    $(".btn-close, .screen-overlay").click(function(e){
    	$(".screen-overlay").removeClass("show");
        $(".mobile-offcanvas").removeClass("show");
        $("body").removeClass("offcanvas-active");
    }); 
    
}); 
// jquery end

