from question import Question

_author_ = "Knut Lucas Andersen"


class CalculateGrade:
    """
    This class calculates the score for a given questionnaire
    based on the set confidence level for each answer. Initialize
    the class by calling __init__, and then call __unicode__ to
    display the result.
    """

    __score = 0.0  # score achieved
    __total_score = 0.0  # total score for this questionnaire
    __grade = None  # grade achieved
    __xblock = None  # container for the XBlock
    __is_score_calculated = False

    def __init__(self, xblock, total_score, question_list):
        """
        Class constructor that initializes objects

        Arguments:
            xblock (XBlock): Object of the parent XBlock class
            total_score (float): Score/points needed to achieve 100%
            question_list (list): Dictionary containing this questionnaires questions

        """
        self.__xblock = xblock
        self.__total_score = total_score
        self.__is_score_calculated = False
        self.__question_list = question_list
        # self.__calculate_grade()

    def __unicode__(self):
        """
        Returns a string object with the achieved score and grade

        Returns:
            str: Result text (score and grade)

        """
        # variable for the grade string
        grade_text = "\nGrade: " + self.__grade
        # variable for the __score string
        score_text = "Your score was: " + str(self.__score) + "%."
        return score_text + grade_text

    def calculate_grade(self):
        """
        Calculates the grade based on the score achieved on this questionnaire
        """
        score = 0.0
        grade_dictionary = self.__xblock.grade_dictionary
        if self.__is_score_calculated is False:
            score = self.__calculate_score()
        # calculate the score in percent
        self.__score = (score / self.__total_score) * 100
        # since score can be over more than 100% and less then 0%, adjust it
        if self.__score > 100:
            self.__score = 100
        elif self.__score < 0:
            self.__score = 0
        # get the grade based on the score
        if self.__score >= grade_dictionary['gradeA']['score']:
            self.__grade = grade_dictionary['gradeA']['grade']
        elif self.__score >= grade_dictionary['gradeB']['score']:
            self.__grade = grade_dictionary['gradeB']['grade']
        elif self.__score >= grade_dictionary['gradeC']['score']:
            self.__grade = grade_dictionary['gradeC']['grade']
        elif self.__score >= grade_dictionary['gradeD']['score']:
            self.__grade = grade_dictionary['gradeD']['grade']
        elif self.__score >= grade_dictionary['gradeE']['score']:
            self.__grade = grade_dictionary['gradeE']['grade']
        else:
            self.__grade = grade_dictionary['gradeF']['grade']
        self.__grade = str(self.__grade)

    def __calculate_score(self):
        """
        Calculates the score based on the submitted answers and selected confidence level.

        This function calculates the score for the questionnaire the student has submitted.
        It loops through all the submitted answers, retrieving both the selected answer and
        the selected confidence level for this answer. The submitted answers are then compared
        against the questions belonging to the questionnaire to see which answers are correct

        See:
            | ``__get_selected_confidence_level_score``: Returns the confidence level for the current question
            | ``__get_current_question``: Returns the question object belonging to the passed question id
            | ``__check_if_answer_is_correct``: Checks if the selected answer is correct

        Returns:
            float: The total score achieved on this questionnaire

        """

        score = 0.0
        # get the students submitted answers and loop through them
        student_answer_dictionary = self.__xblock.student_answer_dictionary
        for details in student_answer_dictionary:
            # get question and confidence level
            question = self.__get_current_question(details.get_question_id())
            confidence_level = self.__get_selected_confidence_level_score(details.get_selected_confidence())
            # check the selected answer(s) for this question and return score
            score += self.__check_if_answer_is_correct(details.get_answer_id(), question, confidence_level)
        return score

    def __get_selected_confidence_level_score(self, selected_confidence_level):
        """
        Returns a dictionary with score values for the current answer.

        Arguments:
            selected_confidence_level (str): The selected confidence level for this question

        Returns:
            dict: Score values for the current answer

        """
        confidence_level_dictionary = self.__xblock.confidenceLevels
        # get and return selected confidence level
        if selected_confidence_level in ['low', 'Low', 'LOW']:
            return confidence_level_dictionary['low']
        elif selected_confidence_level in ['normal', 'Normal', 'NORMAL']:
            return confidence_level_dictionary['normal']
        elif selected_confidence_level in ['high', 'High', 'HIGH']:
            return confidence_level_dictionary['high']

    def __get_current_question(self, question_id):
        """
        Returns the question object matching the passed ```question_id```

        Arguments
            question_id (int): The id of the question object to retrieve

        Returns:
            Question: The Question object

        """

        counter = 0
        question = None
        question_not_found = True
        question_list = self.__question_list
        list_size = len(question_list)
        # loop until the question is found, or all questions are checked
        while question_not_found and counter < list_size:
            current_question_id = question_list[counter].get_question_id()
            if current_question_id == question_id:
                question = question_list[counter]
                question_not_found = False
            counter += 1
        return question

    @staticmethod
    def __check_if_answer_is_correct(answer_id=int, question=Question, confidence_level=dict):
        """
        Checks if the currently selected answer is correct.

        This functions checks if the currently selected answer is correct.
        This is achieved by comparing the selected answer ID the answers
        belonging to this question, to see which one(s) are correct. The score
        for each answer is based on the selected confidence level for this
        question.

        Arguments:
            answer_id (int): The ID of the selected answer
            question (Question): The question the currently selected answer belongs to
            confidence_level (dict): The selected confidence level for this question

        Returns:
            float: The score for this question

        """

        score = 0.0
        # loop through the submitted answers and those belonging to the question
        for current_alternative in question.get_alternatives():
            # if this is one of the submitted answers, check if it is correct
            if current_alternative.get_answer_id() == answer_id:
                if current_alternative.get_is_answer_correct():
                    score += confidence_level['correct']
                else:
                    score += confidence_level['wrong']
        return score

    def get_score(self):
        """
        Returns the score achieved for this questionnaire

        Returns:
            float: Score achieved

        """
        return self.__score

    def get_grade(self):
        """
        Returns the grade achieved on this questionnaire

        Returns:
            str: Grade achieved

        """
        return self.__grade

    def check_if_lists_are_set(self):
        """
        Checks if the lists/dictionaries used have content (for debugging purposes)

        Returns:
             str: String stating whether or not the given lists/dictionaries have content

        """
        # get the dictionaries
        questions_dictionary = self.__question_list
        student_answers_dictionary = self.__xblock.student_answer_dictionary
        grade_dictionary = self.__xblock.grade_dictionary
        confidence_level_dictionary = self.__xblock.confidenceLevels
        # get and return the result
        result = self.__check_status_of_list("Questions", questions_dictionary)
        result += "<br /> " + self.__check_status_of_list("SubmittedAnswers", student_answers_dictionary)
        result += "<br /> " + self.__check_status_of_list("Grades", grade_dictionary)
        result += "<br /> " + self.__check_status_of_list("Confidence Level", confidence_level_dictionary)
        result += "<br /> "
        return result

    def __check_status_of_list(self, name, content_list):
        """
        Checks if the passed list is ```None``` (empty) or has content (for debugging purposes).

        Arguments:
            name (str): The name of this list/dictionary (for text output)
            content_list (obj): The list/dictionary to check

        Returns:
             str: String informing whether or not the list has content

        """
        result = self.__check_if_list_has_content(content_list)
        # check content of passed dictionary
        if result is None:
            status = "Dictionary (" + name + ") is None."
        else:
            status = "Dictionary (" + name + ") " + str(result)
        return status

    @staticmethod
    def __check_if_list_has_content(content_list):
        """
        Checks if the passed list has content or if it is ```None```.
        The function either returns None (if list is empty) or
        a string with the content and the length of the list.
        (for debugging purposes)

        Arguments:
            content_list (obj): List to check

        Returns:
            object: None || String (str)

        """
        content = None
        if content_list is not None:
            content = "Content: " + str(content_list) + " \nLength: " + str(len(content_list))
        return content
