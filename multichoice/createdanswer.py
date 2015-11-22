

class CreatedAnswer(object):
    """
    Class container for question alternatives created by the teacher.
    """

    __answer_id = None
    __answer_text = None
    __is_correct = None

    def __init__(self, answer_id=int, answer_text=str, is_correct=None):
        """
        Constructor for the QuestionAlternatives class.

        Creates an object of the alternative which belongs to a question,
        which also checks if the passed values are set and valid.

        Arguments:
            answer_id (int): ID of this answer
            answer_text (str): The answer description
            is_correct (bool/None): Is this answer the correct one?
        """
        try:
            self.__check_if_alternative_is_valid(answer_id, answer_text, is_correct)
        except ValueError:
            raise
        self.__answer_id = answer_id
        self.__answer_text = answer_text
        self.__is_correct = is_correct

    def get_answer_id(self):
        """
        Returns the ID belonging to this answer.

        Returns:
            int: The ID of this answer
        """
        return self.__answer_id

    def get_answer_text(self):
        """
        Returns the description text for this answer

        Returns:
            str: Description of answer
        """
        return self.__answer_text

    def get_is_answer_correct(self):
        """
        Returns the value for whether or not this is the correct answer

        Returns:
            bool: Value indicating if this answer is correct or wrong
        """
        return self.__is_correct

    @staticmethod
    def __check_if_alternative_is_valid(answer_id, answer_text, is_correct):
        """
        Checks if the passed parameters is set with correct value. Called when creating alternatives only.

        Arguments:
            answer_id (int): ID of the answer alternative
            answer_text (str): Description of this answer alternative
            is_correct (bool): Is this alternative the correct answer

        """
        try:
            int(answer_id)
        except ValueError:
            raise ValueError('Answer alternative (ID) must be a number.')
        if answer_text is None or answer_text is "":
            raise ValueError('The text description of the answer alternative cannot be empty.')
        if type(is_correct) is not bool:
            raise ValueError('Answer alternative must be set to either True or False.')

