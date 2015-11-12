/* Javascript for MultiChoiceXBlock. */
function MultiChoiceXBlock(runtime, element) {

    function invoke(method, data, onSuccess)
    {
	console.log("invoked");
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

        $('#multichoice-qf-save').click(function () {
		var question = $("#multichoice-qf-question").val();
		console.log("The question was " + question);
		$(".multichoice-alterntive-input").each(function(i, obj) {
			// hente verdi fra no i
			// sende til kontroller
		});
		$.ajax({
		    type: "POST",
		    url: runtime.handlerUrl(element, 'save_questions'),
		    data: JSON.stringify({question: question}),
		    success: function(result) {
		        console.log(result)
		    }
               });
		var no = $("#questions_list li").size() + 1;
		$("#questions_list").append("<li data-question=\"" + no + "\"><div class=\"multichoice-question\">" + question + "</div><div class=\"multichoice-x\">x</div><div class=\"clearfix\"></div></li>");

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
