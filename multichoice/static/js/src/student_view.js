function AnswerXBlock(runtime, element){

    window.questionAmount = 0;

    $('.submission > button').click(function (){
        var choices = [];
        var answers = {};
        var questionId = $(this).closest('fieldset').attr('id');
        var $CL = $('input[name=confidence-level-' + questionId + ']:checked');
        var $chosen = $('input[name=answer-' + questionId + ']:checked');
        var $submitButton = $('#submit-question-' + questionId);
        if($chosen.length > 0) {
            if($CL.length > 0) {
                $chosen.each(function () {
                   choices.push($(this).attr('value'))
                });
                var cl_value = $CL.attr('value');
                answers[questionId] = {'chosen': choices, 'confidence': cl_value};
                //console.log(answers);
                invoke('save_student_answers', answers, function(data){
                    console.log(data);
                    $submitButton.attr('disabled', 'disabled');
                    questionAmount++;
                    console.log(questionAmount);
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

    $('#submit-all-questions').click(function(){
        if(questionAmount > 0){
           invoke('get_grade', questionAmount, function(data) {
               $('#grade > p').append(data['grade']);
               $('#grade').show(0);
           })
        }
        else {
            alert('You have to answer at least one question');
        }
    });

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