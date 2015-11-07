/* Javascript for MultiChoiceXBlock. */
function MultiChoiceXBlock(runtime, element) {

    function invoke(method, data, onSuccess)
    {
        var handlerUrl = runtime.handlerUrl(element, method);

        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify(data),
            success: onSuccess
        });

        console.log(handlerUrl);
    }



    $('#add_question').click(function () {

        invoke('add_question', {'hoho': 'ja'}, function (a, b, c) {

            console.log('got it');
            console.log(a);
            console.log(b);
            console.log(c);

        });


    });





    /* old */

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
