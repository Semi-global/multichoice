import pkg_resources


from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List, Dict
from xblock.fragment import Fragment

from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO

class MultiChoiceXBlock(XBlock):

    ''' Studio data '''
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

    ''' Student data '''
    responses = List(
        default=[], scope=Scope.user_state,
    )

    score = Integer(
        default=0, scope=Scope.user_state,
    )


    def studio_view(self, context=None):

        tpl = Template(filename="multichoice/multichoice/static/html/studio.html")
        buf = StringIO()
        ctx = Context(buf, xblock=self)
        tpl.render_context(ctx)

        frag = Fragment(buf.getvalue())
        frag.add_css(self.resource_string("static/css/multichoice.css"))
        frag.add_javascript(self.resource_string("static/js/src/multichoice.js"))
        frag.initialize_js('MultiChoiceXBlock')
        return frag


    ''' Model methods '''

    def addQuestion(self, question, alternatives):

        if not self.isQuestionValid(question, alternatives):
            return False

        for alternative in alternatives:
            if not self.isAlternativeValid(alternative):
                return False

        question = {
            'id': len(self.questions),
            'question': question,
            'alternatives': alternatives
        }

        self.questions.append(question)

        return question

    def isQuestionValid(self, question, alternatives):

        if len(question) == 0:
            return False

        if len(alternatives) == 0:
            return False

        return True


    def isAlternativeValid(self, alternative):

        if type(alternative) is not dict:
            return False

        if alternative.get('text') == None:
            return False

        if len(alternative.get('text')) == 0:
            return False

        if type(alternative.get('isCorrect')) != bool:
            return False

        return True


    ''' JSON handler methods '''

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

        addedQuestion = self.addQuestion(question, answers)

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