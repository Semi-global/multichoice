_author_ = "Knut Lucas Andersen"


class Answer(object):
    """
    Class container for Answer objects.

    The Answer object can either be an answer alternative
    created by a teacher (which then belongs to a question),
    or an answer submitted by a student during a test/questionnaire.
    """

    __answer_id = None
    __answer_text = None
    __is_correct = None
    __selected_confidence_level = None
    __is_creation_mode = None

    def __init__(self, is_creation_mode=bool, answer_id=int, answer_text=str, is_correct=None, selected_confidence_level=None):
        """
        Constructor for the Answer class.

        |  This constructor can be used in two different ways;
        |
        |  1. Answer alternatives for questions created by teacher/lecturer.
        |  If this is an answer alternative created by the teacher, then:
        |  ```is_creation_mode``` should be set to 'True',
        |  ```is_correct``` should be set to either ```True``` or ```False```, and
        |  ```selected_confidence_level``` should be set to ```None```.
        |
        |  2. Answer submitted by student during questionnaire/test.
        |  If this is an answer submitted by the student, then:
        |  ```is_creation_mode``` should be set to 'False',
        |  ```selected_confidence_level``` should be set to one of the given values (low, normal or high).
        |

        Arguments:
            is_creation_mode (bool): If teacher creating question, set to ```True```. Else, ```False```.
            answer_id (int): ID of this answer
            answer_text (str): The answer description
            is_correct (bool/None): Is this answer the correct one?
            selected_confidence_level (None/str):
                |  If alternative for question, then None.
                |  If selected answer by student, then string value of selected confidence level.

         Raises:
            ValueError: Only occurs if ```is_creation_mode``` is set to ```True```
                |  Raises error if ```answer_id``` is not a valid number (int).
                |  Raises error if ```answer_text``` is not a valid number (int).
                |  Raises error if ```is_correct``` is neither True or False.

        """
        try:
            if is_creation_mode:
                self.__check_if_alternative_is_valid(answer_id, answer_text, is_correct)
        except ValueError:
            raise
        self.__answer_id = answer_id
        self.__answer_text = answer_text
        self.__is_correct = is_correct
        self.__selected_confidence_level = selected_confidence_level
        self.__is_creation_mode = is_creation_mode

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

    def get_selected_confidence_level_for_answer(self):
        """
        Returns the selected confidence level for this answer

        Returns:

        """
        return self.__selected_confidence_level

    def get_is_creation_mode(self):
        """
        Returns the value for whether this is an answer created by a teacher,
        or answer submitted by student.

        Returns:
            bool:
                |  True: Alternative created by teacher.
                |  False: Answer submitted by student.
        """
        return self.__is_creation_mode

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
        if answer_text is "":
            raise ValueError('The text description of the answer alternative cannot be empty.')
        if is_correct is not True and is_correct is not False:
            raise ValueError('Answer alternative must be set to either True or False.')

