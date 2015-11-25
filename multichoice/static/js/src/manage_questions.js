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
            multichoiceqc.addAlternative(-1, '', false);
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
    $('.question > [data-id="' + id + '"').parent().remove();
    for (key in this.questions)
    {
        if (this.questions[key].id == id)
            this.questions.splice(key, 1);
    }
    this.focusQuestion(-1);
    return;

    invoke('remove_question', id, function(data) {
        $('.question > [data-id="' + id + '"').parent().remove();

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

    $('#multichoice-loading').hide();
    $('#multichoice-layout > nav').show();

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
    $('#multichoice-alternatives').empty();
    for (var key in activeQuestion.alternatives)
    {
        this.addAlternative(activeQuestion.alternatives[key].id, activeQuestion.alternatives[key].text, activeQuestion.alternatives[key].isCorrect);
    }



    $('.question').removeClass('active-question');
    $('.question > [data-id="' + activeQuestion.id + '"').parent().addClass('active-question');


}


MultichoiceQuestionController.prototype.addAlternative = function (id, alternative, isCorrect) {

    var that = this;
    $container = $('#multichoice-alternatives');
    $alternatives = $container.find('input[type=\'text\']');
    if ($alternatives.size() == 0) // only text
        $container.empty();

    if (isCorrect)
    {
        isCorrect = 1; // to int
        iconClass = 'fa-thumbs-o-up';
    }
    else
    {
        isCorrect = 0; // to int
        iconClass = 'fa-thumbs-o-down';
    }

    var idx = $('.multichoice-alternative-input').size();

    var $alternative = $('<div><span class="multichoice-x">x</span><input type="hidden" name="multichoice-alternative-iscorrect-' + idx + '" id="multichoice-alternative-iscorrect-' + idx + '" value="' + isCorrect + '" /><input type="text" name="multichoice-alternative-text-' + idx + '" class="multichoice-alternative-input" value="' + alternative + '" /><i class="toggle fa ' + iconClass + '"></i></div>');
    $container.append($alternative);

    $alternative.find('.multichoice-x').click(function (e) {
        $(e.target).parent().remove();
    });

    $alternative.find('.toggle').click(function (e) {

        var $i = $(e.target);

        if ($i.hasClass('fa-thumbs-o-up'))
        {
            $i.removeClass('fa-thumbs-o-up');
            $i.addClass('fa-thumbs-o-down');
            $('#multichoice-alternative-iscorrect-' + idx).val(1);
        }
        else
        {
            $i.removeClass('fa-thumbs-o-down');
            $i.addClass('fa-thumbs-o-up');
            $('#multichoice-alternative-iscorrect-' + idx).val(0);
        }

    });


}

MultichoiceQuestionController.prototype.setMessage = function (message, isError) {

    var $error = $('#multichoice-errormessage');
    var $ok = $('#multichoice-okmessage');
    var $target = null;

    $error.hide();
    $ok.hide();

    if (isError)
        $target = $error;
    else
        $target = $ok;

    $target.html(message);
    $target.show();
}

MultichoiceQuestionController.prototype.setQuestions = function (questions) {
    this.questions = questions;
    console.log(questions);
}

MultichoiceQuestionController.prototype.populateQuestions  = function () {

    var that = this;
    $ul = $('#multichoice-layout > nav > ul');
    $ul.empty();

    for (key in this.questions)
    {
        $ul.append('<li class="question"><div class="multichoice-question" data-id="' + this.questions[key].id + '">' + this.questions[key].question + '</div><div class="multichoice-x" data-id="' + this.questions[key].id + '">x</div><div class="clearfix"></div></li>');
    }

    $('.multichoice-x').click(function (e) {

        var remove = confirm('Do you really want to delete the question?');

        if (!remove)
            return;

        var id = $(e.target).data('id');
        multichoiceqc.removeQuestion(id);
    });

    $('.multichoice-question').click(function (e) {

        var id = $(e.target).data('id');
        that.focusQuestion(id);
    });

    this.focusQuestion(-1);

}