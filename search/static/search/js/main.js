/* It's a small function for to spawn print of the spinner */
function connect() {
    $('#spinner').show(600);
}

/* This condition is used to adjust the readability of the errors in the registration form */
if (document.getElementsByClassName('error')) {
    $(".error").toggleClass("result_error");
}

/* This condition is used to adjust the readability of the errors in the login form */
if (document.getElementById('error_login')) {
    $("#error_login").toggleClass("result_error");
}

/* These code line use js for change the input on page top */
document.getElementById('id_food');
{
    $('#id_food').toggleClass("color_find_base");
}

/* This method is use for change the error message if email is use */
if (document.getElementsByClassName('errorlist')) {
    const user = $('.error').text();
    if (user.indexOf('User') === 9) {
        $('div div div div div div div p').first().replaceWith(
            '<p id="result_error" class="result_error">'
            + 'Cette adresse email est déjà utilisée.' + '</p>');

    }
}

/* The purpose of these functions below is to allow
enlarging and / or shrinking the images in description */
function zoom_pics_1() {
    document.getElementById('pics_1').style.width = '400px';
    document.getElementById('pics_1').style.height = '420px';

    document.getElementById('pics_2').style.width = '250px';
    document.getElementById('pics_2').style.height = '220px';

    document.getElementById('pics_3').style.width = '250px';
    document.getElementById('pics_3').style.height = '220px';
}

function zoom_pics_2() {
    document.getElementById('pics_2').style.width = '400px';
    document.getElementById('pics_2').style.height = '420px';

    document.getElementById('pics_1').style.width = '250px';
    document.getElementById('pics_1').style.height = '220px';

    document.getElementById('pics_3').style.width = '250px';
    document.getElementById('pics_3').style.height = '220px';
}

function zoom_pics_3() {
    document.getElementById('pics_3').style.width = '400px';
    document.getElementById('pics_3').style.height = '420px';

    document.getElementById('pics_1').style.width = '250px';
    document.getElementById('pics_1').style.height = '220px';

    document.getElementById('pics_2').style.width = '250px';
    document.getElementById('pics_2').style.height = '220px';
}


/* This function allows you to be from US to FR language */
if (document.getElementsByName('submit')) {
    $("input").attr("src", "https://www.paypal.com/fr_FR/i/btn/btn_buynowCC_LG.gif");
}


var disabledDates = ["28-06-2020", "21-06-2020"]


/* This function allow of manage the booking dates of the user */
$(function datepicker() {

    /* Get the available dates */

    $(".datepicker").datepicker({

        /* Check the available dates */
        beforeShowDay: function (date) {
            var string = jQuery.datepicker.formatDate('dd-mm-yy', date);
            return [disabledDates.indexOf(string) == -1]
        },

        /* Configure DatePicker settings */
        altField: "#datepicker",
        closeText: 'Fermer',
        prevText: 'Précédent',
        nextText: 'Suivant',
        currentText: 'Aujourd\'hui',
        monthNames: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
        monthNamesShort: ['Janv.', 'Févr.', 'Mars', 'Avril', 'Mai', 'Juin', 'Juil.', 'Août', 'Sept.', 'Oct.', 'Nov.', 'Déc.'],
        dayNames: ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'],
        dayNamesShort: ['Lun.', 'Mar.', 'Mer.', 'Jeu.', 'Ven.', 'Sam.', 'Dim.'],
        dayNamesMin: ['L', 'M', 'M', 'J', 'V', 'S', 'D'],
        weekHeader: 'Sem.',
        dateFormat: 'dd-mm-yy',
        minDate: 0,

        /* Get the choice of the user */
        onSelect: function (date) {
            if (this.id === 'datepicker_to_go') {
                /* Block the min date for the max date field */
                var minDate = $('#datepicker_to_go').datepicker('getDate');
                $("#datepicker_return").datepicker("change", {minDate: minDate});
            }

            if (this.id === 'datepicker_return') {
                /* Block the max date for the min date field */
                var maxDate = $('#datepicker_return').datepicker('getDate');
                $("#datepicker_to_go").datepicker("change", {maxDate: maxDate});
            }
        }
    });
});


/* The function below record a click of the user
She records the click that selects a non-registered
    favorite food and will indicate it to the system to create the record */


$(document).ready(function () {
    if (document.getElementsByClassName('datepicker')) {
        var url = window.location.href;
        console.log(url);
        $.get("date_min.txt", function (data) {
            console.log(data)
        }, 'text')
    }
})
