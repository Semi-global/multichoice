function AnswerXBlock(runtime, element){

    $('.submit-button').click(function (){
        var choices = [];
        var questionId = $(this).closest('fieldset').attr('id');
        var $CL = $('input[name=confidence-level-' + questionId + ']:checked');
        var $chosen = $('input[name=answer-' + questionId + ']:checked');
        if($chosen.length > 0) {
            if($CL.length > 0) {
                $chosen.each(function () {
                   choices.push($(this).attr('value'))
                });
                invoke('save_student_answers', {'questionId': questionId, 'chosen': choices, 'confidence': $CL.attr('value')}, function(data){
                    console.log(data);
                    for (key in data) {
                        var $correct = $('#q' + questionId + '-check-' + key);
                        var $wrong = $('#q' + questionId + '-times-' + key);
                        console.log(data[key]);
                        if (data[key] == "true")
                            $correct.show(0);
                        else
                            $wrong.show(0);
                    }
                })
            }
            else {
                alert('Choose your confidence level')
            }
        }
        else {
            alert('Make your choice')
        }
    });

    //$('.question-checkbox').click(function (){
    //    var choices = [];
    //    var questionId = $(this).closest('fieldset').attr('id');
    //    console.log(questionId);
    //    //var $confidenceLevel = $('input[name=confidence-level-' +questionId + ']:checked');
    //    var $chosen = $('input[name=answer-' + questionId + ']:checked');
    //    console.log($chosen.length);
    //    if($chosen.length > 0) {
    //        $chosen.each(function () {
    //           choices.push($(this).attr('id'))
    //        });
    //        answers[questionId] = {'chosen': choices};
    //        console.log(answers[1]);
    //        console.log(answers[2]);
    //    }
    //});

    function displayResult(data){

    }

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


}