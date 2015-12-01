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

        multichoiceqc = new MultichoiceQuestionController();

        invoke('get_questions', null, function(data) {
            multichoiceqc.setQuestions(data);
            multichoiceqc.populateQuestions();
        });

        $('#multichoice-qf-add-alternative').click(function () {
            multichoiceqc.addAlternative('', false, -1);
        });

           //Listens for when a student has been selected:
        $('.student-container').click(function(){
            var studentClickedId = parseInt($(this).find('.student-id').attr("id"));              //Retrieves ID of clicked student.

            console.log("Student clicked: "+studentClickedId);

            $('.questionnaire-review').fadeTo('fast', 0.3).fadeTo('fast', 1.0);     //Fades clicked student to indicate seleciton

            //All students except the one clicked has its background set to white:
            $('.student-container').each(function( index ) {
                $(this).css("background-color", "white");
            });
            $(this).css("background-color", "#fc9a24")                              //The one clicked gets new background color to show selection.

            invoke('get_answers', null, function(data) {                //Calla for method get_answers
                //multichoiceqc.get_answers();
                //console.log(data)
             var currentId = "";

            $(".question-alternative").each(function( index ) {
            console.log("clearing question")
               $(this).prop("checked", false);
             //  $(this).prop("disabled", true);
            });

            $(".confidence-alternative").each(function( index ) {
                console.log("clearing confidence")
               $(this).prop("checked", false);
            });

            $(".difficulty-level-alternative").each(function( index ) {
                console.log("clearing difficulty")
               $(this).prop("checked", false);
            });


            $.each(data, function(index, student) {             //Goes through each returned students
                currentId = student.id;

                if(currentId == studentClickedId) {             //If the clicked student is found på by ID
                   console.log("Should be correct student")
                   console.log(student);

                    var bufferQId;
                   $.each(student.questions, function(index, question) {        //Goes through all submitted answers belonging to student
                       //console.log(index, question)
                       //console.log(index-1)

                       //TODO match question number to questionnaire and select them to show what student answered.

                            bufferQId = question-1;

                       $('.question-container').eq((index-1)).find('.question-alternative').eq(bufferQId).prop("checked", true);

                   });


                   $.each(student.confidence, function(index, confidenceAlt) {        //Goes through all submitted confidence levels
                        console.log("Confidence", index)
                        $('.confidence-container').eq(index).find('.confidence-alternative').eq(confidenceAlt).prop("checked", true);
                   });

                  $.each(student.difficulty, function(index, difficultyAlt) {        //Goes through all submitted difficulty levels
                        console.log("Difficulty", index)
                        $('.difficulty-level-container').eq(index).find('.difficulty-level-alternative').eq(difficultyAlt).prop("checked", true);
                   });


                }

            });

           })

        });



    });



}

var multichoiceqc = null;


var MultichoiceQuestionController = function () {
}

MultichoiceQuestionController.prototype.questions = [];

MultichoiceQuestionController.prototype.addAlternative = function (alternative, isCorrect, id) {
    $container = $('#multichoice-alternatives');
    $alternatives = $container.find('input[type=\'text\']');
    if ($alternatives.size() == 0) // only text
        $container.empty();

    console.log($alternatives.size());

    $container.append('<div><span class="multichoice-x">x</span><input type="text" class="multichoice-alterntive-input" data-id="' + id + '" value="' + alternative + '" /><i class="fa fa-thumbs-o-up"></i></div>');

}

MultichoiceQuestionController.prototype.setQuestions = function (questions) {
    this.questions = questions;
}

MultichoiceQuestionController.prototype.populateQuestions  = function () {

    $ul = $('#multichoice-layout > nav > ul');
    $ul.empty();

    for (key in this.questions)
    {
        $ul.append('<li data-question="' + this.questions[key].id + '"><div class="multichoice-question">' + this.questions[key].question + '</div><div class="multichoice-x">x</div><div class="clearfix"></div></li>');
    }

}