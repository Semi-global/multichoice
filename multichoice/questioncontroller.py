class QuestionController:

    XBlock = None

    questions = [
        {
            'id': 1,
            'question': 'Choose A, B or C',
            'alternatives': [{
                'id': '1',
                'text': 'A',
                'isCorrect': True
            }, {
                'id': '2',
                'text': 'B',
                'isCorrect': False
            }, {
                'id': '3',
                'text': 'C',
                'isCorrect': False
            }]
        },
        {
            'id': 2,
            'question': 'Choose D, E or F',
            'alternatives': [{
                'id': '1',
                'text': 'D',
                'isCorrect': True
            }, {
                'id': '2',
                'text': 'E',
                'isCorrect': False
            }, {
                'id': '3',
                'text': 'F',
                'isCorrect': False
            }]
        }
    ]

    # questions = []

    def __init__(self, XBlock):
        self.XBlock = XBlock

    def get_questions(self):
        return self.questions

    def add_question(self, question):

        if not self.__is_question_valid(question):
            return False

        self.questions.append(question)

        return question

    @staticmethod
    def __is_question_valid(self, question, alternatives):

        if len(question) == 0:
            return False

        if len(alternatives) == 0:
            return False

        return True


    def __isAlternativeValid(self, alternative):

        if type(alternative) is not dict:
            return False

        if alternative.get('text') == None:
            return False

        if len(alternative.get('text')) == 0:
            return False

        if type(alternative.get('isCorrect')) != bool:
            return False

        return True
