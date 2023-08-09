/**
 * Fade out and remove alert messages after a specified delay.
 */
window.setTimeout(function () {
    $(".alert").fadeTo(500, 0).slideUp(500, function () {
        $(this).remove();
    });
}, 4000);

/**
 * Execute code when the document is ready.
 */
$(document).ready(function () {
    /**
     * Fade out and remove alert messages after a specified delay.
     */
    window.setTimeout(function () {
        $(".alert").fadeTo(500, 0).slideUp(500, function () {
            $(this).remove();
        });
    }, 5000);
});
