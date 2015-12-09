import unittest
from xblock.core import XBlock
from question import Question

class test_question(unittest.TestCase):

    def setUp(self):
        self.q = Question(1, "some text", True)


    def test_set_question_text(self):
        self.q.set_question_text("test is best")
        assert self.q.get_question_text() == "test is best"

    def test_set_has_difficulty_level(self):
        self.q.set_has_difficulty_level(True)
        assert self.q.get_has_difficulty_level() == True

    def test_add_alternative(self):
        self.q.add_alternative(0, "An alternative", True)
        self.q.add_alternative(1, "An alternative 2", False)
        alternatives = self.q.get_alternatives();
        assert len(alternatives) == 2

    def test_add_alternative_negative(self):
        self.q.add_alternative("A", "An alternative", True)
        alternatives = self.q.get_alternatives()
        assert len(alternatives) == 0

    def test_is_valid(self):
        self.q.set_question_text("test is best")
        self.q.add_alternative(0, "An alternative", True)
        self.q.add_alternative(1, "An alternative 2", False)
        valid = self.q.is_valid()
        assert valid == True

    def test_to_json(self):
        self.q.set_question_text("test is best")
        self.q.add_alternative(0, "An alternative", True)
        json = self.q.to_json()
        assert "id" in json
        assert "question" in json
        assert "alternatives" in json
        assert "has_difficulty_level" in json
        assert "id" in json["alternatives"][0]
        assert "text" in json["alternatives"][0]
        assert "isCorrect" in json["alternatives"][0]

        assert json["id"] == 1
        assert json["question"] == "test is best"
        assert json["has_difficulty_level"] == True
        assert json["alternatives"][0]["id"] == 0
        assert json["alternatives"][0]["text"] == "An alternative"
        assert json["alternatives"][0]["isCorrect"] == True
