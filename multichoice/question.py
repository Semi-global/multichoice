def is_alternative_valid(alternative):
        if alternative['id'] is '':
            return False
        elif alternative['text'] is '':
            return False
        elif alternative['isCorrect'] is '':
            return False
        else:
            return True


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
        if alt_id is not str:
            alt_id = str(alt_id)
        alternative = {
            'id': alt_id,
            'text': alt_text,
            'isCorrect': alt_correct
        }
        if is_alternative_valid(alternative):
            self.alternatives.append(alternative)
            return False
        else:
            return True

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
