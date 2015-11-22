var invoke = null;

/* Javascript for MultiChoiceXBlock. */
function MultiChoiceXBlock(runtime, element) {

    $(document).ready(function () {

        multichoiceqc = new MultichoiceQuestionController();

        invoke('get_questions', null, function(data) {
            multichoiceqc.setQuestions(data);
            multichoiceqc.populateQuestions();
        });

        $('#multichoice-qf-add-alternative').click(function () {
            multichoiceqc.addAlternative('', false, -1);
        });

    });

    invoke = function (method, data, onSuccess)
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

var multichoiceqc = null;


var MultichoiceQuestionController = function () {
}

MultichoiceQuestionController.prototype.questions = [];

MultichoiceQuestionController.prototype.removeQuestion = function (id) {

    console.log('remove when ready');
    $('.question[data-id="' + id + '"').remove();
    for (key in this.questions)
    {
        if (this.questions[key].id == id)
            this.questions.splice(key, 1);
    }
    this.focusQuestion(-1);
    return;

    invoke('remove_question', id, function(data) {
        $('.question[data-id="' + id + '"').remove();

        for (key in this.questions)
        {
            if (this.questions[key].id == id)
                this.questions.splice(key, 1);
        }

        this.focusQuestion(-1);
    });

}

MultichoiceQuestionController.prototype.focusQuestion = function (id) {

    var activeQuestion = null;
    var firstQuestion = null;
    for (var key in this.questions)
    {
        if (!firstQuestion)
            firstQuestion = this.questions[key];

        if (this.questions[key].id == id)
            activeQuestion = this.questions[key];

    }

    if (!activeQuestion && firstQuestion)
        activeQuestion = firstQuestion;

    if (!activeQuestion)
    {
        $('#multichoice-questionform').hide();
        $('#multichoice-no-questions-added').show();
        return;
    }

    $('#multichoice-questionform').show();
    $('#multichoice-no-questions-added').hide();

    $('#multichoice-qf-question').val(activeQuestion.question);
    // set alternatives


    $('.question').removeClass('active-question');
    $('.question[data-id="' + activeQuestion.id + '"').addClass('active-question');


}


MultichoiceQuestionController.prototype.addAlternative = function (alternative, isCorrect, id) {
    $container = $('#multichoice-alternatives');
    $alternatives = $container.find('input[type=\'text\']');
    if ($alternatives.size() == 0) // only text
        $container.empty();

    console.log($alternatives.size());

    $container.append('<div><span class="multichoice-x" data-id="' + id + '">x</span><input type="text" class="multichoice-alterntive-input" data-id="' + id + '" value="' + alternative + '" /><i class="fa fa-thumbs-o-up"></i></div>');

}

MultichoiceQuestionController.prototype.setQuestions = function (questions) {
    this.questions = questions;
    console.log(questions);
}

MultichoiceQuestionController.prototype.populateQuestions  = function () {

    $ul = $('#multichoice-layout > nav > ul');
    $ul.empty();

    for (key in this.questions)
    {
        $ul.append('<li class="question" data-id="' + this.questions[key].id + '"><div class="multichoice-question">' + this.questions[key].question + '</div><div class="multichoice-x" data-id="' + this.questions[key].id + '">x</div><div class="clearfix"></div></li>');
    }


    $('.multichoice-x').click(function (e) {

        var remove = confirm('Do you really want to delete the question?');

        if (!remove)
            return;

        var id = $(e.target).data('id');
        multichoiceqc.removeQuestion(id);
    });

    this.focusQuestion(-1);

}