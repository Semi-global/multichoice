from answer import Answer

class Question(object):

    id = None
    question = None
    alternatives = []
    # alternative = {
    #     'id': '',
    #     'text': '',
    #     'isCorrect': None
    # }
    has_difficulty_level = None

    def __init__(self, question_id,  question, difficulty_level):
        self.question_id = question_id
        self.question_text = question
        self.has_difficulty_level = difficulty_level

    def get_question_id(self):
        return self.question_id

    def get_question_text(self):
        return self.question_text

    def get_has_difficulty_level(self):
        return self.has_difficulty_level

    def add_alternative(self, alt_id, alt_text, alt_correct):
        try:
            creation_mode = True  # value indicating this is teacher alternative
            answer = Answer(creation_mode, alt_id, alt_text, alt_correct)
            self.alternatives.append(answer)
            return True
        except ValueError as e:
            print(e)  # TODO: Add error handling here

    def get_alternatives(self):
        return self.alternatives

    def is_valid(self):
        if self.question_id is not int or self.question_id is None:
            return False
        elif self.question_text is "" or self.question_text is None:
            return False
        elif self.has_difficulty_level is None:
            return False
        elif len(self.alternatives) < 2:
            return False
        else:
            return True
