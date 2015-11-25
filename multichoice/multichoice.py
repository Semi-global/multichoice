import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List, Dict
from xblock.fragment import Fragment

from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO

from calculategrade import CalculateGrade
from question import Question
from submittedanswers import SubmittedAnswer

# TODO: This might be needed by Dmytro/Khai for creating/storing Teachers added alternatives
from createdanswer import CreatedAnswer


class MultiChoiceXBlock(XBlock):
    """ Studio data """
    ''' Use self.questionController.<somemethod/attr> to work with these variables'''

    title = String(
        default="", scope=Scope.content,
    )

    description = String(
        default="", scope=Scope.content,
    )

    questions_json_list = List(
        default=[
            {
                'id': 0,
                'question': 'Choose A, B or C',
                'alternatives': [{
                    'id': '0',
                    'text': 'A',
                    'isCorrect': True
                }, {
                    'id': '1',
                    'text': 'B',
                    'isCorrect': False
                }, {
                    'id': '2',
                    'text': 'C',
                    'isCorrect': False
                }],
                'has_difficulty_level': True
            },
            {
                'id': 1,
                'question': 'Choose D, E or F',
                'alternatives': [{
                    'id': '0',
                    'text': 'D',
                    'isCorrect': True
                }, {
                    'id': '1',
                    'text': 'E',
                    'isCorrect': False
                }, {
                    'id': '2',
                    'text': 'F',
                    'isCorrect': False
                }],
                'has_difficulty_level': False
            }
        ]
        , scope=Scope.content,
    )

    question_objects_list = List(
        default=[],
        scope=Scope.content,
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
        SubmittedAnswer(2, 1, 'high'),
        SubmittedAnswer(2, 2, 'high')
        ]

    def __init__(self, *args, **kwargs):
        super(XBlock, self).__init__(*args, **kwargs)
        # self.xmodule_runtime = self.runtime
        # self.questionController = QuestionController(self)

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

    def _is_answer_correct(self, answer_id=int):
        """
        Looks for the answer in the questions dictionary and returns correctness value of the answer.

        Arguments:
            answer_id (str): string value of the answer ID.

        Returns:
            bool: correctness value for a particular answer.
        """

        for question in self.questions_json_list:
            for alternative in question['alternatives']:
                if alternative['id'] == answer_id:
                    return alternative['isCorrect']

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
            # get the list containing the questions,
            # and check if its empty (if so, fill with default values)
            question_list = self.question_objects_list
            # TODO: This may have to be removed at a later time
            if (question_list is None) or (len(question_list) is 0):
                question_list = self.get_default_question_objects()
            # get the number of questions, and set this as total score, then calculate the grade
            total_score = len(question_list)
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
        return self.questions_json_list

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
        try:
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
                    return {'status': 'Not saved', 'message': 'Alternative is not valid'}

            if new_question.is_valid:
                self.question_objects_list.append(new_question)
                self.questions_json_list.append(new_question.to_json())
                num_questions = len(self.questions_json_list)
                question = self.questions_json_list[num_questions - 1]
                return {'status': 'successful', 'numQuestions': num_questions, 'question': question}
            else:
                return{'status': 'unsuccessful', 'message': 'Question data is not valid'}
        except Exception as ex:
            return {'status': 'unsuccessful', 'message': str(ex)}

    ''' Helper methods '''

    @XBlock.json_handler
    def delete_question(self, data, suffix=''):
        """
        Deletes question with data['question_id'] from both JSON and Object lists

        :param data: JSON object passed from the view with the ID of the that needs to be deleted.
                     Example: data = {'question_id': 0'}
        :param suffix: None
        :return: JSON object with status and exception text if caught.
        """

        try:
            self.questions_json_list.remove(int(data['question_id']))
            self.question_objects_list.remove(int(data['question_id']))
            return {'status': 'successful'}
        except Exception as ex:
            return {'status': 'unsuccessful', 'message': str(ex), 'id': int(data['question_id'])}

    @XBlock.json_handler
    def update_field(self, data, suffix=''):
        """
        Updates question fields.

        :param data: JSON object passed from the view. Should contain ID of the question, field name and value.
                     Example: data = {
                                         'question_id': 0,
                                         'field': 'question',
                                         'value': 'How much is 2x2?'
                                     }
        :param suffix: None
        :return: JSON object with status and exception text if caught.
        """

        try:
            q_id = int(data['question_id'])
            self.questions_json_list[q_id][str(data['field'])] = data['value']
            # question_object = self.question_objects_list[int(data['question_id'])]
            if data['field'] is 'id':
                self.question_objects_list[q_id].set_question_id(data['value'])
            elif data['field'] is 'question':
                self.question_objects_list[q_id].set_question_text(data['value'])
            elif data['field'] is 'has_difficulty_level':
                self.question_objects_list[q_id].set_has_difficulty_level(data['value'])
            return {'status': 'successful'}
        except Exception as ex:
            return {'status': 'unsuccessful', 'message': str(ex)}

    @XBlock.json_handler
    def add_alternative(self, data, suffix=''):
        """
        Adds alternative to the question

        :param data: JSON object passed from the view with question ID, alternative ID and all alternative data.
                     Example: data = {
                                         'question_id': 0,
                                         'alt_id': 0,
                                         'text': 'First alternative',
                                         'icCorrect': true
                                     }

        :param suffix: None
        :return: JSON object with status and exception text if caught.
        """

        try:
            q_id = int(data['question_id'])
            alt_id = int(data['alt_id'])
            self.questions_json_list[q_id]['alternatives']['id'] = alt_id
            self.questions_json_list[q_id]['alternatives']['text'] = str(data['text'])
            self.questions_json_list[q_id]['alternatives']['isCorrect'] = bool(data['isCorrect'])
            self.question_objects_list[q_id].add_alternative(alt_id, str(data['text']), bool(data['isCorrect']))
            return {'status': 'successful'}
        except Exception as ex:
            return {'status': 'unsuccessful', 'message': str(ex)}

    @XBlock.json_handler
    def update_alternatives(self, data, suffix=''):
        """
        Updates alternatives for the question

        :param data: JSON object passed from the view with question ID, alternative ID and all alternative data.
                     Example: data = {
                                         'question_id': 0,
                                         'alt_id': 0,
                                         'text': 'First alternative',
                                         'icCorrect': true
                                     }

        :param suffix: None
        :return: JSON object with status and exception text if caught.
        """

        try:
            q_id = int(data['question_id'])
            alt_id = int(data['alt_id'])
            self.questions_json_list[q_id]['alternatives'][alt_id]['text'] = data['text']
            self.questions_json_list[q_id]['alternatives'][alt_id]['isCorrect'] = bool(data['isCorrect'])
            self.question_objects_list[q_id].remove_alternative(alt_id)
            self.question_objects_list[q_id].add_alternative(alt_id, data['text'], bool(data['isCorrect']))
            return {'status': 'successful'}
        except Exception as ex:
            return {'status': 'unsuccessful', 'message': str(ex)}

    @XBlock.json_handler
    def delete_alternative(self, data, suffix=''):
        """
        Deletes alternative for the question

        :param data: JSON object passed from the view with question and alternative IDs.
                     Exapmple: data = {
                                          'question_id': 0,
                                          'alt_id': 0
                                      }
        :param suffix: None
        :return: JSON object with status and exception text if caught.
        """

        try:
            q_id = int(data['question_id'])
            alt_id = int(data['alt_id'])
            self.questions_json_list[q_id]['alternatives'].remove(alt_id)
            self.question_objects_list[q_id].remove_alternative(alt_id)
            return {'status': 'successful'}
        except Exception as ex:
            return {'status': 'unsuccessful', 'message': str(ex)}

    # def reload_questions(self):
    #     self.questions_json_list[:] = []
    #     for q in self.question_objects_list:
    #         self.questions_json_list.append(q.to_json())

    @staticmethod
    def get_default_question_objects():
        """
        Creates a list which is returned, this is to be used as default option in
        the list ```question_objects_list```

        Returns:
            list: A list with default question objects
        """
        question_list = list()
        question1 = Question(1, 'Choose A, B or C', False)
        question1.add_alternative(1, 'A', True)
        question1.add_alternative(2, 'B', False)
        question1.add_alternative(3, 'C', False)
        question_list.append(question1)
        question2 = Question(2, 'Choose D, E or F', False)
        question2.add_alternative(1, 'D', True)
        question2.add_alternative(2, 'E', False)
        question2.add_alternative(3, 'F', False)
        question_list.append(question2)
        return question_list

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
