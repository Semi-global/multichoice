var multichoiceqc = null;

function initMultiChoiceXBlock(runtime, element) {

    multichoiceqc = new MultichoiceQuestionController(runtime, element);

    multichoiceqc.fetchQuestionsFromServer();

    $('#multichoice-qf-add-alternative').click(function () {
        multichoiceqc.addAlternative(-1, '', false);
    });

    $('#multichoice-save-question').click(function () {
        if (multichoiceqc.validateQuestion())
            multichoiceqc.saveQuestion();

        return false;
    });

    $('#multichoice-add-question').click(function () {
        multichoiceqc.focusQuestion(-1, true);
    });

    return true;
}


/* Javascript for MultiChoiceXBlock. */
function MultiChoiceXBlock(runtime, element) {
    $(document).ready(function () {
        initMultiChoiceXBlock(runtime, element);
    });
}


var MultichoiceQuestionController = function (runtime, element) {
    this.runtime = runtime;
    this.element = element;
}

MultichoiceQuestionController.prototype.questions = [];
MultichoiceQuestionController.prototype.runtime = null;
MultichoiceQuestionController.prototype.element = null;


MultichoiceQuestionController.prototype.fetchQuestionsFromServer = function () {

    var that = this;
    this.invoke('get_questions', null, function(data) {
        that.setQuestions(data);
        that.populateQuestions();
    });

}

MultichoiceQuestionController.prototype.invoke = function (method, data, onSuccess)
{
    var handlerUrl = this.runtime.handlerUrl(this.element, method);

    $.ajax({
        type: "POST",
        url: handlerUrl,
        data: JSON.stringify(data),
        success: onSuccess
    });
}


MultichoiceQuestionController.prototype.removeQuestion = function (id) {

    var that = this;

    this.invoke('delete_question', {question_id: id}, function(data) {

        if (data == null || data == undefined || data.status != 'successful')
        {
            that.setMessage('Could not remove question: ' + data.message, true);
        }
        else
        {
            $('.question > [data-id="' + id + '"').parent().remove();

            for (key in that.questions)
            {
                if (that.questions[key].id == id)
                    that.questions.splice(key, 1);
            }

            that.focusQuestion(-1, false);
            that.setMessage('Question removed', false);
        }
    });

}

MultichoiceQuestionController.prototype.focusQuestion = function (id, isNew) {

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

    if (isNew)
        activeQuestion = null;

    if (!activeQuestion && !isNew)
    {
        $('#multichoice-questionform').hide();
        $('#multichoice-no-questions-added').show();
        return null;
    }

    $('#multichoice-questionform').show();
    $('#multichoice-no-questions-added').hide();

    $('#multichoice-alternatives').empty();
    $('.question').removeClass('active-question');


    if (activeQuestion)
    {
        $('#multichoice-question-id').val(activeQuestion.id);
        $('#multichoice-qf-question').val(activeQuestion.question);

        if (activeQuestion.has_difficulty_level)
            $('#multichoice-difficulty-level').prop('checked', true);
        else
            $('#multichoice-difficulty-level').prop('checked', false);

        for (var key in activeQuestion.alternatives)
        {
            this.addAlternative(activeQuestion.alternatives[key].id, activeQuestion.alternatives[key].text, activeQuestion.alternatives[key].isCorrect);
        }

        $('.question > [data-id="' + activeQuestion.id + '"').parent().addClass('active-question');

    }
    else
    {
        $('#multichoice-question-id').val(-1);
        $('#multichoice-qf-question').val('');
    }

    return activeQuestion;
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

    var $alternative = $('<div class="multichoice-alternative"><span class="multichoice-x">x</span><input type="hidden" class="multichoice-alternative-id" value="' + id + '" /><input type="hidden" class="multichoice-alternative-iscorrect" value="' + isCorrect + '" /><input type="text" class="multichoice-alternative-text" value="' + alternative + '" /><i class="toggle fa ' + iconClass + '"></i></div>');
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
            $i.parent().find('.multichoice-alternative-iscorrect').val(0);
        }
        else
        {
            $i.removeClass('fa-thumbs-o-down');
            $i.addClass('fa-thumbs-o-up');
            $i.parent().find('.multichoice-alternative-iscorrect').val(1);
        }

    });


}

MultichoiceQuestionController.prototype.hideMessage = function () {

    var $error = $('#multichoice-errormessage');
    var $ok = $('#multichoice-okmessage');

    $error.hide();
    $ok.hide();
}


MultichoiceQuestionController.prototype.setMessage = function (message, isError) {

    var $error = $('#multichoice-errormessage');
    var $ok = $('#multichoice-okmessage');
    var $target = null;

    this.hideMessage();

    if (isError)
        $target = $error;
    else
        $target = $ok;

    $target.html(message);
    $target.show();
}

MultichoiceQuestionController.prototype.validateQuestion = function () {
    var error = '';
    var foundIncorrectAlternatives = 0;
    var foundCorrectAlternatives = 0;

    this.hideMessage();

    var question = $('#multichoice-qf-question').val();

    if (question.length == 0)
        error = 'Question is missing';

    $('.multichoice-alternative').each(function () {

        var $e = $(this);
        var alternativeText = $e.find('.multichoice-alternative-text').val();
        var isCorrect = $e.find('.multichoice-alternative-iscorrect').val();

        if (alternativeText.length == 0)
        {
            error = 'Empty alternative';
            return;
        }

        if (isCorrect == 0)
            foundIncorrectAlternatives++;
        else
            foundCorrectAlternatives++;

    });

    if (error.length == 0)
    {
        if ((foundCorrectAlternatives + foundIncorrectAlternatives) < 2)
            error = 'Too few alternatives';

        if (foundCorrectAlternatives < 1)
            error = 'No correct alternative added';

    }

    if (error.length > 0)
    {
        this.setMessage(error, true);
        return false;
    }


    return true;
}

MultichoiceQuestionController.prototype.saveQuestion = function () {

    var that = this;
    var alternatives = [];

    $('.multichoice-alternative').each(function () {

        var $e = $(this);
        var alternativeText = $e.find('.multichoice-alternative-text').val();
        var isCorrect = parseInt($e.find('.multichoice-alternative-iscorrect').val());
        var id = $e.find('.multichoice-alternative-id').val();

        if (isCorrect == 1)
            isCorrect = true;
        else
            isCorrect = false;

        alternatives.push({
            id: id,
            text: alternativeText,
            isCorrect: isCorrect
        });
    });

    var hasDifficultyLevel = $('#multichoice-difficulty-level').prop('checked');

    var question = {
        id: $('#multichoice-question-id').val(),
        text: $('#multichoice-qf-question').val(),
        alternatives: alternatives,
        hasDifficultyLevel: hasDifficultyLevel
    };

    this.invoke('save_question', question, function(data) {

        if (data == undefined || data.status != 'successful')
        {
            that.setMessage('Could not remove question: ' + data.message, true);
        }
        else
        {
            that.setMessage('Question saved', false);

            that.invoke('get_questions', null, function(data) {
                multichoiceqc.setQuestions(data);
                multichoiceqc.populateQuestions();

                if (data.question != undefined && data.question.id != undefined)
                    that.focusQuestion(data.question.id);
            });
        }
    });
}


MultichoiceQuestionController.prototype.setQuestions = function (questions) {
    this.questions = questions;
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
        that.focusQuestion(id, false);
    });

    this.focusQuestion(-1, false);

}