import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List, Dict
from xblock.fragment import Fragment

from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO

from questioncontroller import QuestionController
from calculategrade import CalculateGrade
from question import Question
from submittedanswers import SubmittedAnswer

# TODO: This might be needed by Dmytro/Khai for creating/storing Teachers added alternatives
from createdanswer import CreatedAnswer


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
    student_answers = {}

    score = Integer(
        default=0, scope=Scope.user_state,
    )

    has_score = False

    questionInterface = None

    # TODO: The following is the example of how answers submitted by students is expected to look
    # TODO: question_id, answer_id, confidence_level (can select more than one alternative too
    student_answer_dictionary = [
        SubmittedAnswer(1, 2, 'low'),
        SubmittedAnswer(1, 3, 'low'),
        SubmittedAnswer(2, 4, 'high'),
        SubmittedAnswer(2, 5, 'high')
        ]

    def __init__(self, *args, **kwargs):
        super(XBlock, self).__init__(*args, **kwargs)
        self.xmodule_runtime = self.runtime
        self.questionController = QuestionController(self)

    @property
    def get_questions_prop(self):
        return self.questionController.get_questions()

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

    def student_view(self, context=None):
        tpl = Template(filename="multichoice/multichoice/static/html/student_view.html")
        buf = StringIO()
        ctx = Context(buf, xblock=self)
        tpl.render_context(ctx)

        frag = Fragment(buf.getvalue())
        frag.add_css(self.resource_string("static/css/student_view.css"))
        frag.add_javascript(self.resource_string("static/js/src/student_view.js"))
        frag.initialize_js('AnswerXBlock')
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
    def save_student_answers(self, data, suffix=''):
        """
        Saves student answers passed from the student view,
        and returns a dictionary with correctness of the answers back to student

        Arguments:
            data: a dictionary that contains question ID, alternatives chosen by the student,
                and confidence level of the student.
                data =  {
                            questionId: {
                                chosen: [1, 2],
                                confidence: 'High'
                            }
                        }
        Returns:
            dict: a dictionary containing answer ID and corresponding correctness.
                dict =  {
                            1: 'true',
                            2: 'false'
                        }
        """
        for i in data:
            self.student_answers[i] = data[i]
            return_data = {}
            for answer_id in self.student_answers[i]['chosen']:
                if self._is_answer_correct(answer_id):
                    return_data[answer_id] = 'true'
                else:
                    return_data[answer_id] = 'false'

            return return_data

    @XBlock.json_handler
    def get_grade(self, data, suffix=''):
        """
        Retrieves the score and grade for the questionnaire based
        on the students submitted answers. This achieved by calling
        the class ``CalculateGrade`` and the function ``__unicode__``
        which returns a string with the score and grade.

        Arguments:
            data:
            suffix:

        See:
            ``CalculateGrade.__unicode__``

        Returns:
            object: JSON object containing the string with the score and grade

        """
        grade = ''
        try:
            # get the dictionary containing the questions and set the total score
            question_list = self.questionController.get_questions()
            total_score = len(question_list)
            # create an object of the class that calculates the grade
            calc_grade = CalculateGrade(self, total_score, question_list)
            # This is for debugging, in case it does not work
            # (checks if dictionaries has content)
            # grade = calc_grade.check_if_lists_are_set()
            # print the grade
            grade = calc_grade.__unicode__()
        except Exception, ex:
                grade += "<p>An exception occurred: " + str(ex) + ". "
                grade += "Failed at calculating grade."
        return {'grade': grade}

    @XBlock.json_handler
    def get_questions(self, data, suffix=''):
        return self.questionController.get_questions()

    @XBlock.json_handler
    def add_question(self, data, suffix=''):
        """
        Adds question to question collection stored in ``QuestionController`` class.
        :param data: JSON object that contains question in a format:
                data = {
                    question: {
                        'id': 1,
                        'text': 'Text',
                        'alternatives': [
                            {
                                'id': '1',
                                'text': 'Text',
                                'isCorrect': 'false'
                            },
                            {
                                'id': '2',
                                'text': 'Text2',
                                'isCorrect': 'false'
                            },
                            ...
                        ],
                        'hasDifficultyLevel: 'false'
                    }
                }
        :param suffix:
        :return: JSON object with the size of questions collection and last added question
        """

        q_id = int(data[0]['id'])
        q_text = data[0]['text']
        if data[0]['hasDifficultyLevel'] is 'true':
            q_has_diff_lvl = True
        else:
            q_has_diff_lvl = False

        new_question = Question(q_id, q_text, q_has_diff_lvl)

        for a in data[0]['alternatives']:
            # TODO: Note that the called function in CreatedAnswers throws error
            # TODO: See comment in Question::add_alternative
            if not new_question.add_alternative(a['id'], a['text'], a['isCorrect']):
                return {'status': 'Not saved'}

        if new_question.is_valid:
            self.questionController.add_question(new_question)
            num_questions = len(self.get_questions_prop)
            question = self.get_questions_prop[num_questions - 1]
            return {'status': 'Saved', 'numQuestions': num_questions, 'question': question}
        else:
            return{'status': 'Not saved'}

    ''' Helper methods '''
    def _is_answer_correct(self, answer_id):
        """
        Looks for the answer in the questions dictionary and returns correctness value of the answer.

        Arguments:
            answer_id (str): string value of the answer ID.

        Returns:
            bool: correctness value for a particular answer.
        """
        for question in self.get_questions_prop:
            for alternative in question['alternatives']:
                if alternative['id'] == answer_id:
                    return alternative['isCorrect']

    @staticmethod
    def resource_string(path):
        """ Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    @staticmethod
    def get_progress(self):
        return None

    @staticmethod
    def workbench_scenarios():
        return [
            ("MultiChoiceXBlock",
             """<multichoice/>
             """),
        ]
