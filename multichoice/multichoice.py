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
    """
    The confidence level for each question, ranging from low to high.
    The score goes from 0 and 1 for low, up to -1 and 2 for high.
    The score received is based on whether or not the selected answer(s)
    were correct. Used in ```CalculateGrade```

    See:
      |  ```CalculateGrade```
    """

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
    """
    Dictionary containing the grades available, from A - F,
    with the relevant score for each grade. Used in ```CalculateGrade```

    See:
      |  ```CalculateGrade```
    """

    student_answer_dictionary = []
    """
    This dictionary contains the current student answers to the given questionnaire.
    For grade to be calculated properly, it expects objects of the class ```SubmittedAnswers```

    See:
      |  ```SubmittedAnswers```
      |  ```CalculateGrade```
    """

    title = String(
        default="", scope=Scope.content,
    )

    description = String(
        default="", scope=Scope.content,
    )

    questions_json_list = List(
        default=[
            # {
            #     'id': 0,
            #     'question': 'Choose A, B or C',
            #     'alternatives': [{
            #         'id': '0',
            #         'text': 'A',
            #         'isCorrect': True
            #     }, {
            #         'id': '1',
            #         'text': 'B',
            #         'isCorrect': False
            #     }, {
            #         'id': '2',
            #         'text': 'C',
            #         'isCorrect': False
            #     }],
            #     'has_difficulty_level': True
            # },
            # {
            #     'id': 1,
            #     'question': 'Choose D, E or F',
            #     'alternatives': [{
            #         'id': '0',
            #         'text': 'D',
            #         'isCorrect': True
            #     }, {
            #         'id': '1',
            #         'text': 'E',
            #         'isCorrect': False
            #     }, {
            #         'id': '2',
            #         'text': 'F',
            #         'isCorrect': False
            #     }],
            #     'has_difficulty_level': False
            # }
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

    student_name = "Lars"
    student_id = Integer(
        default=123, scope=Scope.content,
    )

    #student_answerArray = [1, 1, 2]

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


    #Dummy array for answers, based on available questions 1. dec
    students_sub = [
        {
            "id": "1",              #Identifies student
            "questions": {          #List of alternatives chosen by student.
                1: 1,               #Question number and the corresponding chosen alternative
                2: 3
            },
            "confidence": {
                0: 0,     #not confident
                1: 2      #im certain
            },
            "difficulty": {
                0: 1       #above average
            }

        },
        {
            "id": "2",
            "questions": {
                1: 3,
                2: 1
            },
            "confidence": {
                0: 1,
                1: 0
            },
            "difficulty": {
                0:0
            }
        }
    ]

    student_ans = [[1,1,1,1], [2,2,2,2]]

    ''' Student data '''
    student_answers = list()

    score = Integer(
        default=0, scope=Scope.user_state
    )

    has_score = False

    questionInterface = None

    def __init__(self, *args, **kwargs):
        super(XBlock, self).__init__(*args, **kwargs)
        if self.questions_json_list is None or len(self.questions_json_list) is 0:
            self.questions_json_list = self.get_default_questions_json()
            # if self.question_objects_list is None or len(self.question_objects_list) is 0:
            #     self.question_objects_list = self.get_default_questions_json()
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

    @XBlock.json_handler                            #Returns array with all students that have submitted answers:
    def get_answers(self, data, suffix=''):
        return self.students_sub



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

        self.student_answers.append(data)
        return_data = {}
        # print data['question_id']
        for answer_id in data['chosen']:
            answer_obj = SubmittedAnswer(int(data['question_id']), int(answer_id), data['confidence'])
            self.student_answer_dictionary.append(answer_obj)
            if self._is_answer_correct(int(answer_id), int(data['question_id'])):
                return_data[answer_id] = 'true'
            else:
                return_data[answer_id] = 'false'

        return return_data

    def _is_answer_correct(self, answer_id=int, question_id=int):
        """
        Looks for the answer in the questions dictionary and returns correctness value of the answer.

        Arguments:
            answer_id (int): string value of the answer ID.

        Returns:
            bool: correctness value for a particular answer.
        """

        for alternative in self.questions_json_list[question_id]['alternatives']:
            print alternative
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
            question_list = self.create_object_from_json()
            total_score = len(question_list)
            calc_grade = CalculateGrade(self, total_score, question_list)
            # This is for debugging, in case it does not work
            # (checks if dictionaries has content)
            # grade = calc_grade.check_if_lists_are_set()
            calc_grade.calculate_grade()
            # print the grade
            grade += calc_grade.__unicode__()
        except Exception, ex:
            grade += "<p>An exception occurred: " + str(ex) + ". "
            grade += "Failed at calculating grade."
        return {'grade': grade, 'answers': data}

    @XBlock.json_handler
    def get_questions(self, data, suffix=''):
        return self.questions_json_list

    @XBlock.json_handler
    def save_question(self, data, suffix=''):
        """
        Adds question to question collection stored in ``QuestionController`` class.
        :param data: JSON object that contains question in a format:
                data = {
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
                        'hasDifficultyLevel': 'false'
                }
        :param suffix:
        :return: JSON object with the size of questions collection and last added question
        """
        try:
            q_id = int(data['id'])
            q_text = data['text']
            if data['hasDifficultyLevel']:
                q_has_diff_lvl = True
            else:
                q_has_diff_lvl = False

            new_question = Question(q_id, q_text, q_has_diff_lvl)

            for i in range(0, len(data['alternatives'])):
                # TODO: Note that the called function in CreatedAnswers throws error
                # TODO: See comment in Question::add_alternative
                if not new_question.add_alternative(i, data['alternatives'][i]['text'], data['alternatives'][i]['isCorrect']):
                    return {'status': 'Not saved', 'message': 'Alternative is not valid'}

            if new_question.is_valid:
                if q_id < 0:
                    new_question.set_question_id(len(self.questions_json_list))
                    self.questions_json_list.append(new_question.to_json())
                else:
                    for i in range(0, len(self.questions_json_list)):
                        if self.questions_json_list[i]['id'] == q_id:
                            del self.questions_json_list[i]
                            self.questions_json_list.insert(i, new_question.to_json())

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
        q_id = int(data['question_id'])
        try:
            for i in range(0, len(self.questions_json_list)):
                # print self.questions_json_list[i]['id']
                # print q_id
                if self.questions_json_list[i]['id'] == q_id:
                    del self.questions_json_list[i]
                    break
            return {'status': 'successful'}
        except Exception as ex:
            return {'status': 'unsuccessful', 'message': str(ex), 'pos': self.questions_json_list[0],
                    'index': q_id}

    @staticmethod
    def get_default_question_objects():
        """
        Creates a list which is returned, this is to be used as default option in
        the list ```question_objects_list```

        Returns:
            list: A list with default question objects
        """
        question_list = list()
        question1 = Question(0, 'Choose A, B or C', False)
        question1.add_alternative(0, 'A', True)
        question1.add_alternative(1, 'B', False)
        question1.add_alternative(2, 'C', False)
        question_list.append(question1)
        question2 = Question(1, 'Choose D, E or F', False)
        question2.add_alternative(0, 'D', False)
        question2.add_alternative(1, 'E', False)
        question2.add_alternative(2, 'F', True)
        question_list.append(question2)
        return question_list

    @staticmethod
    def get_default_questions_json():
        question_list = list()
        question1 = Question(0, 'Choose A, B or C', True)
        question1.add_alternative(0, 'A', False)
        question1.add_alternative(1, 'B', True)
        question1.add_alternative(2, 'C', False)
        question_list.append(question1.to_json())
        question2 = Question(1, 'Choose D, E or F', False)
        question2.add_alternative(0, 'D', False)
        question2.add_alternative(1, 'E', False)
        question2.add_alternative(2, 'F', True)
        question_list.append(question2.to_json())
        return question_list

    @staticmethod
    def resource_string(path):
        """ Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def create_object_from_json(self):
        """
        Creates a list of Question objects from the JSON dictionary questions_json_list

        Returns:
            list: List containing objects of the class Questions

        """
        question_list = list()
        # loop through all the json questions and add them to the list
        for json_question in self.questions_json_list:
            q_id = json_question['id']
            q_text = json_question['question']
            q_diff_lvl = json_question['has_difficulty_level']
            question = Question(q_id, q_text, q_diff_lvl)
            # loop through all the alternatives for this question and add them
            for alt in json_question['alternatives']:
                a_id = alt['id']
                a_text = alt['text']
                a_is_correct = alt['isCorrect']
                question.add_alternative(a_id, a_text, a_is_correct)
            # add the question object to the list
            question_list.append(question)
        return question_list

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
