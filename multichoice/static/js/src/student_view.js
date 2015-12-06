function AnswerXBlock(runtime, element){

    window.questionAmount = 0;

    $(document).ready(function(){

    });

    $('.submission > button').click(function (){
        var choices = [];
        var answers = {};
        var questionId = $(this).closest('fieldset').attr('id');
        var $CL = $('input[name=confidence-level-' + questionId + ']:checked');
        var $chosen = $('input[name=answer-' + questionId + ']:checked');
        var $submitButton = $('#submit-question-' + questionId);
        var $diff_level = $('#sa-' + questionId).find('input[name=difficulty-level-' + questionId + ']:checked');
        var $is_diff_level = $('#sa-' + questionId).find('.difficulty-level');
        if($chosen.length > 0) {
            if($CL.length > 0) {
                if ($is_diff_level.length > 0 && $diff_level.length == 0) {
                    alert('Please choose difficulty level for this question');
                    return false;
                }
                else if ($is_diff_level.length > 0 && $diff_level.length >0) {
                    answers['difficulty_level'] = $diff_level.attr('value');
                }
                $chosen.each(function () {
                   choices.push($(this).attr('value'))
                });
                var cl_value = $CL.attr('value');
                answers['question_id'] = questionId;
                answers['chosen'] = choices;
                answers['confidence'] = cl_value;
                console.log("answers: \n");
                console.log(answers);
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
            //TODO: @DMYTRO,
            //TODO: this is just testcode to show it works, so move this where its relevant
           invoke('grade_students_difficulty_level', {'amount': questionAmount}, function(data) {
               $('#grade > p').append(data['result']);
               $('#grade').show(0);
               console.log("result", data['result'])

           });
            //TODO - END: @DMYTRO
           invoke('get_grade', {'amount': questionAmount}, function(data) {
               $('#grade > p').append(data['grade']);
               $('#grade').show(0);
               console.log(data['q'])
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