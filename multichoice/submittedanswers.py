

class SubmittedAnswer(object):
    """
    Class container for answers submitted by students.
    """

    __question_id = None
    __answer_id = None
    __selected_confidence_level = None

    def __init__(self, question_id=int, answer_id=int, selected_confidence_level=str):
        """
        Constructor creating an object of the selected answer submitted by the student

        Arguments:
            question_id: The ID of the question which this answer belongs to
            answer_id: The ID of the selected answer
            selected_confidence_level: The confidence level selected for this answer

        """
        self.__question_id = question_id
        self.__answer_id = answer_id
        self.__selected_confidence_level = selected_confidence_level

    def get_question_id(self):
        """
        Returns the ID of the question this answer belongs to.

        Returns:
            int: The question ID
        """
        return self.__question_id

    def get_answer_id(self):
        """
        Returns the ID belonging to this answer.

        Returns:
            int: The ID of this answer
        """
        return self.__answer_id

    def get_selected_confidence(self):
        """
        Returns the selected confidence level for this answer

        Returns:

        """
        return self.__selected_confidence_level

