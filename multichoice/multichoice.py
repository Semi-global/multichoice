import pkg_resources


from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List, Dict
from xblock.fragment import Fragment
from classes.questions import Questions

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