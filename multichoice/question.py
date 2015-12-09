from createdanswer import CreatedAnswer


class Question(object):

    question_id = None
    question = None
    # For format, see CreatedAnswers::__init__
    # alternative = {
    #     'id': '',
    #     'text': '',
    #     'isCorrect': None
    # }
    has_difficulty_level = None

    def __init__(self, question_id=int,  question=str, difficulty_level=bool):
        self.question_id = question_id
        self.question_text = question
        self.has_difficulty_level = difficulty_level
        self.alternatives = list()

    def get_question_id(self):
        return self.question_id

    def get_question_text(self):
        return self.question_text

    def get_has_difficulty_level(self):
        return self.has_difficulty_level

    def add_alternative(self, alt_id=int, alt_text=str, alt_correct=None):
        try:
            answer = CreatedAnswer(int(alt_id), str(alt_text), bool(alt_correct))
            self.alternatives.append(answer)
            return True
        except ValueError as e:
            return False

    def get_alternatives(self):
        return self.alternatives

    def set_question_id(self, question_id):
        self.question_id = question_id

    def set_question_text(self, question_text):
        self.question_text = question_text

    def set_has_difficulty_level(self, has_diff_level):
        self.has_difficulty_level = has_diff_level

    def remove_alternative(self, alternative_id):
        self.alternatives.remove(alternative_id)

    def is_valid(self):
        if isinstance(1, int) == False or self.question_id is None:
            return False
        elif self.question_text is "" or self.question_text is None:
            return False
        elif self.has_difficulty_level is None:
            return False
        elif len(self.alternatives) < 2:
            return False
        else:
            return True

    def to_json(self):
        json = dict()
        json['id'] = self.question_id
        json['question'] = self.question_text
        json['alternatives'] = list()
        for a in self.alternatives:
            json['alternatives'].append({
                'id': a.get_answer_id(),
                'text': a.get_answer_text(),
                'isCorrect': a.get_is_answer_correct()
            })
        json['has_difficulty_level'] = self.has_difficulty_level
        return json
