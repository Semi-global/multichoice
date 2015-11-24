function AnswerXBlock(runtime, element){

    window.questionAmount = 0;

    $(document).ready(function(){
       //invoke('get_questions', null, function(data){
       //    console.log(data);
       //    for(var i=0; i < data.length; i++) {
       //        if(data[i]['has_difficulty_level'] == true){
       //            $('#sa-'+data[i]['id'])
       //                .append('<div class="difficulty-level" id="dl-' + data[i]['id'] + '">' +
       //                         + '<p>How difficult was this question?</p>' +
       //                         + '<input class="dl-radio" type="radio" name="difficulty-level-' + data[i]['id'] + '" id="DL-0" value="Below average"/><label for="DL-0">Below average</label><br/>' +
       //                         + '<input class="dl-radio" type="radio" name="difficulty-level-' + data[i]['id'] + '" id="DL-1" value="Above average"/><label for="DL-1">Above average</label><br/>' +
       //                        '</div>')
       //        }
       //        //console.log(data[i]['has_difficulty_level']);
       //    }
       //})
    });

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
                answers['question'+questionId] = {'question_id': questionId, 'chosen': choices, 'confidence': cl_value};
                console.log(answers['question1']);
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
           invoke('get_grade', {'amount': questionAmount}, function(data) {
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