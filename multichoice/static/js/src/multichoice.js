/* Javascript for MultiChoiceXBlock. */
function MultiChoiceXBlock(runtime, element) {

    function updateCount(result) {
        $('.count', element).text(result.count);
    }

    var handlerUrl = runtime.handlerUrl(element, 'increment_count');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"hello": "world"}),
            success: updateCount
        });
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });

    $('#crap').click(function () {

        $.ajax({
            type: "POST",
            url: runtime.handlerUrl(element, 'xxxinc'),
            data: JSON.stringify({"doit": 1})
        });


    });
}
