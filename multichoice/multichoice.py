import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List, Dict
from xblock.fragment import Fragment

from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO

from questioncontroller import QuestionController


class MultiChoiceXBlock(XBlock):
    ''' Studio data '''
    ''' Use self.questionController.<somemethod/attr> to work with these variables'''

    title = String(
        default="", scope=Scope.content,
    )

    description = String(
        default="", scope=Scope.content,
    )

    questions = List(
        default=[], scope=Scope.content,
    )

    maxScore = Integer(
        default=0, scope=Scope.content,
    )

    confidenceLevels = Dict(
        default={
            'low': {
                'correct': 1,
                'wrong': 0
            },
            'normal': {
                'correct': 1.5,
                'wrong': -0.5
            },
            'high': {
                'correct': 2,
                'wrong': -1
            }
        }, scope=Scope.content,
    )

    # just some estimations for usage
    grade_dictionary = Dict(
        default={
            'gradeA': {'grade': 'A', 'score': 90},
            'gradeB': {'grade': 'B', 'score': 80},
            'gradeC': {'grade': 'C', 'score': 50},
            'gradeD': {'grade': 'D', 'score': 40},
            'gradeE': {'grade': 'E', 'score': 35},
            'gradeF': {'grade': 'F', 'score': 0},
        }, scope=Scope.content,
    )

    student_name = "Lars"
    student_id = Integer(
        default=123, scope=Scope.content,
    )

    student_answerArray = [1, 1, 2]


    students = [
        {
            "ID": "1",
            "Firstname": "Trym",
            "Lastname": "Hansen",
            "Grade": "B"
        },
        {
            "ID": "2",
            "Lastname": "Marlie",
            "Firstname" : "Hella",
            "Grade": "D"
        }
    ]

    student_ans = [[1,1,1,1], [2,2,2,2]]

    ''' Student data '''
    responses = List(
        default=[], scope=Scope.user_state,
    )

    score = Integer(
        default=0, scope=Scope.user_state,
    )

    questionInterface = None

    def __init__(self, *args, **kwargs):
        super(XBlock, self).__init__(*args, **kwargs)
        self.questionController = QuestionController(self)

    ''' Views '''

    def studio_view(self, context=None):
        tpl = Template(filename="multichoice/multichoice/static/html/manage_questions.html")
        buf = StringIO()
        ctx = Context(buf, xblock=self)
        tpl.render_context(ctx)

        frag = Fragment(buf.getvalue())
        frag.add_css(self.resource_string("static/css/multichoice.css"))
        frag.add_css(self.resource_string("static/css/font-awesome.min.css"))
        frag.add_javascript(self.resource_string("static/js/src/manage_questions.js"))
        frag.initialize_js('MultiChoiceXBlock')
        return frag

    def author_view(self, context=None):
        tpl = Template(filename="multichoice/multichoice/static/html/review_stud_quest.html")
        buf = StringIO()
        ctx = Context(buf, xblock=self)
        tpl.render_context(ctx)

        frag = Fragment(buf.getvalue())
        frag.add_css(self.resource_string("static/css/multichoice.css"))
        frag.add_css(self.resource_string("static/css/font-awesome.min.css"))
        frag.add_javascript(self.resource_string("static/js/src/questionnaire_review.js"))
        frag.initialize_js('MultiChoiceXBlock')
        return frag

    ''' JSON handler methods '''

    @XBlock.json_handler
    def get_questions(self, data, suffix=''):
        return self.questionController.getQuestions()

    @XBlock.json_handler
    def add_question(self, data, suffix=''):
        question = 'Choose A, B or C'
        answers = []

        answers.append({
            'text': 'A',
            'isCorrect': True
        })
        answers.append({
            'text': 'B',
            'isCorrect': False
        })
        answers.append({
            'text': 'C',
            'isCorrect': False
        })

        addedQuestion = self.questionController.addQuestion(question, answers)

        return {'numQuestions': len(self.questions), 'question': addedQuestion}

    ''' Helper methods '''

    def resource_string(self, path):
        """ Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @staticmethod
    def workbench_scenarios():
        return [
            ("MultiChoiceXBlock",
             """<multichoice/>
             """),
        ]
