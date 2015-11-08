class QuestionController:

    XBlock = None

    def __init__(self, XBlock):
        self.XBlock = XBlock


    def addQuestion(self, question, alternatives):

        if not self.isQuestionValid(question, alternatives):
            return False

        for alternative in alternatives:
            if not self.isAlternativeValid(alternative):
                return False

        question = {
            'id': len(self.XBlock.questions),
            'question': question,
            'alternatives': alternatives
        }

        self.XBlock.questions.append(question)

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
