$(document).ready(function () {
    // Automatically dismiss flash messages after 5 seconds
    setTimeout(function () {
        $("#flash-message").fadeOut("slow");
    }, 5000);

    // Allow manual dismissal of flash messages
    $('.alert-dismissible .close').on('click', function () {
        $(this).closest('.alert').fadeOut('slow');
    });
});
