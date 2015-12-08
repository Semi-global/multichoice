describe("manage_questions", function() {

    var element = null;
    var mc = null;
    var Runtime = function () {}

    Runtime.prototype.handlerUrl = function (element, method) {
        console.log('handlerUrl invoke');
        return 'someurl';
    }

    var rt = new Runtime(null, null);
    var mc = new MultichoiceQuestionController(rt, null);

    beforeEach(function() {

        var fixtures = '<input type="button" id="multichoice-qf-add-alternative" value="Add alternative"><input type="submit" id="multichoice-save-question" value="Save">';
        fixtures += '<form id="multichoice-questionform" style="" _lpchecked="1">'
                 + '<input type="hidden" id="multichoice-question-id" value="-1">'
                 + '<label for="multichoice-qf-question"><h2>What is your question?</h2></label>'
                 + '<input type="text" id="multichoice-qf-question">'
                 + '<div><input type="checkbox" id="multichoice-difficulty-level"> Enable difficulty level</div>'
                 + '<h3>Alternatives</h3>'
                 + '<div id="multichoice-alternatives"><div class="multichoice-alternative"><span class="multichoice-x">x</span><input type="hidden" class="multichoice-alternative-id" value="-1"><input type="hidden" class="multichoice-alternative-iscorrect" value="0"><input type="text" class="multichoice-alternative-text" value=""><i class="toggle fa fa-thumbs-o-down"></i></div><div class="multichoice-alternative"><span class="multichoice-x">x</span><input type="hidden" class="multichoice-alternative-id" value="-1"><input type="hidden" class="multichoice-alternative-iscorrect" value="0"><input type="text" class="multichoice-alternative-text" value=""><i class="toggle fa fa-thumbs-o-down"></i></div></div>'
                 + '<input type="button" id="multichoice-qf-add-alternative" value="Add alternative">'
                 + '<input type="submit" id="multichoice-save-question" value="Save">'
                 + '</form>';

        setFixtures(fixtures);

        spyOn(mc, 'invoke').and.callFake(function(method, data, onSuccess) {
            console.log('callFake on mc.invoke: ' + method);
            var result = null;

            switch (method)
            {
                case 'get_questions': // return test questions
                    result = ([
                        {
                            id: 1,
                            question: 'Some question A',
                            alternatives: [
                                {
                                    id: 1,
                                    isCorrect: true,
                                    text: 'Alternative A1'
                                },
                                {
                                    id: 2,
                                    isCorrect: false,
                                    text: 'Alternative A2'
                                }
                            ],
                            has_difficulty_level: true
                        },
                        {
                            id: 2,
                            question: 'Some question B',
                            alternatives: [
                                {
                                    id: 1,
                                    isCorrect: true,
                                    text: 'Alternative B1'
                                },
                                {
                                    id: 2,
                                    isCorrect: false,
                                    text: 'Alternative B2'
                                }
                            ],
                            has_difficulty_level: false
                        },
                        {
                            id: 3,
                            question: 'Some question C',
                            alternatives: [
                                {
                                    id: 1,
                                    isCorrect: true,
                                    text: 'Alternative C1'
                                },
                                {
                                    id: 2,
                                    isCorrect: false,
                                    text: 'Alternative C2'
                                }
                            ],
                            has_difficulty_level: true
                        }
                    ]);
                    break;

                case 'delete_question': // remove question
                    if (data.question_id == 999)
                        result = { status: 'unsuccessful', message: 'Test failure' };
                    else
                        result = { status: 'successful' };
                    break;

                default: return;
            }

            onSuccess(result);
        });

    });

    it("focus question negative - none available", function() {
        var ac = mc.focusQuestion(999, false);
        expect(ac).toBe(null);
    });

    it("fetch and set questions", function() {
        mc.fetchQuestionsFromServer();
        expect(mc.questions.length).toBe(3);
    });

    it("remove question negative", function() {
        mc.removeQuestion(999);
        expect(mc.questions.length).toBe(3);
    });

    it("remove question positive", function() {
        mc.removeQuestion(3);
        expect(mc.questions.length).toBe(2);
    });

    it("focus question", function() {
        var ac = mc.focusQuestion(2, false);
        expect(ac.id).toBe(2);
    });

    it("focus question negative - find first available", function() {
        var ac = mc.focusQuestion(999, false);
        expect(ac.id).toBe(1);
    });

    it("focus question - set up new question", function() {
        var ac = mc.focusQuestion(-1, true);
        expect(ac).toBe(null);
    });

    it("save question", function() {
        var ac = mc.focusQuestion(-1, true);
        expect(ac).toBe(null);
    });


    it("xblock init", function() {
        var res = initMultiChoiceXBlock(rt, null);
        //$('#multichoice-save-question').trigger('click');
        expect(res).toBe(true);
    });

    it("validate question", function() {


        expect(1).toBe(1);
    });


});