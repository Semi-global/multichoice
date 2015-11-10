class QuestionController:

    XBlock = None

    def __init__(self, XBlock):
        self.XBlock = XBlock

    def get_questions(self):
        return self.XBlock.questions

    def add_question(self, question, alternatives):

        if not self.__is_question_valid(question, alternatives):
            return False

        for alternative in alternatives:
            if not self.__is_alternative_valid(alternative):
                return False

        question = {
            'id': len(self.XBlock.questions),
            'question': question,
            'alternatives': alternatives
        }

        self.XBlock.questions.append(question)

        return question

    @staticmethod
    def __is_question_valid(question, alternatives):

        if len(question) == 0:
            return False

        if len(alternatives) == 0:
            return False

        return True

    @staticmethod
    def __is_alternative_valid(alternative):

        if type(alternative) is not dict:
            return False

        if alternative.get('text') is None:
            return False

        if len(alternative.get('text')) == 0:
            return False

        if type(alternative.get('isCorrect')) != bool:
            return False

        return True
