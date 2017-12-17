$(document).on('click', 'a[href^="#"]', function(event) {
    event.preventDefault();

    $('html, body').animate({
        scrollTop: $($.attr(this, 'href')).offset().top
    }, 500);
});

$.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
});

function add_unit() {
    var unit_name = $('#subject-form>input[type=text]').val().toUpperCase();
    $.post('/add_unit', {unit:unit_name}).done(function(response) {
        console.log(response);
        switch (response) {
            case '0':
                $('.current-subjects').append(
                '<div class="current-subject" id="subject-' + unit_name + '">' +
                    '<span>' + unit_name + '</span>' +
                    '<i class="material-icons" onclick="return remove_unit("' + unit_name + '")">clear</i>' +
                '</div>'
                );
                unit_name = $('#subject-form>input[type=text]').val("");
                get_calendar();
                break;
            case '1':
                $('.reason').text('UNKNOWN UNIT');
                $('.reason').removeClass('hidden');
                break;
            case '2':
                $('.reason').text('ALREADY ADDED');
                $('.reason').removeClass('hidden');
                break;
            default:
                break;
        }
    });
    return false;
}
function remove_unit(unit) {
    $.post('/remove_unit', {unit:unit}).done(function() {
        $("#subject-" + unit).remove();
        get_calendar();
    });
    return false;
}
function get_calendar() {
    $.get('/generate_monthly').done(function(response) {
        $('.monthly-container').html(response);
    });
    $.get('/generate_weekly').done(function(response) {
        $('.weekly-container').html(response);
    });
}
$(document).ready(function() {
    // get_calendar();
});


var popup_shown = false;
$('.task-popup').hide();
$('.screen-blur').hide();

$('.task').click(function(event) {
    $('.task-popup>.unit-code').html($('.unit-code', this).html());
    $('.task-popup>.unit-desc').html($('.unit-desc', this).html());
    $('.task-popup>.task-desc').html($('.task-desc', this).html());
    $('.screen-blur').show(100);
    $('.task-popup').show(100);
});

$('.event-text').click(function(event) {
    $('.task-popup>.unit-code').html(
        $('span', this).length + " Event" + (($('span', this).length > 1) ? 's' : '')
    );
    $('.task-popup>.unit-desc').html($('.events', this).html());
    $('.task-popup>.task-desc').html("");
    $('.screen-blur').show(100);
    $('.task-popup').show(100);
});

$('.screen-blur').click(function(event) {
    $('.task-popup').hide(100, function() {
        $('.screen-blur').hide();
    });
});

$('.monthly-selector').click(function() {
    $('.weekly-container').css('display', 'none');
    $('.monthly-container').css('display', 'grid');
    $('.monthly-selector, .weekly-selector').toggleClass('active');
});
$('.weekly-selector').click(function() {
    $('.weekly-container').css('display', 'grid');
    $('.monthly-container').css('display', 'none');
    $('.monthly-selector, .weekly-selector').toggleClass('active');
});

