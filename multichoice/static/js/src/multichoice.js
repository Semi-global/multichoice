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
    }

    $(document).ready(function () {
        invoke('get_questions', null, function(data) {
            populateQuestions(data);
        });
    });



    $('#add_question').click(function () {

        invoke('add_question', {'hoho': 'ja'}, function (data) {

            console.log('got it');
            console.log(a);
            console.log(b);
            console.log(c);

        });


    });

}


function populateQuestions(questions) {


    console.log(questions);

    $ul = $('#multichoice-layout > nav > ul');

    for (key in questions)
    {
        $ul.append('<li><div class="multichoice-question">' + questions[key].question + '</div><div class="multichoice-x">x</div><div class="clearfix"></div></li>');
    }


}