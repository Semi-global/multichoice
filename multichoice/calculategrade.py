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
    __question_dictionary = None  # container for the questions asked

    def __init__(self, xblock, total_score, question_dictionary):
        """
        Class constructor that initializes objects

        Arguments:
             xblock (XBlock): Object of the parent XBlock class
            total_score (float): Score/points needed to achieve 100%
            question_dictionary (dict): Dictionary containing this questionnaires questions

        """
        self.__xblock = xblock
        self.__total_score = total_score
        self.__is_score_calculated = False
        self.__question_dictionary = question_dictionary

    def __unicode__(self):
        """
        Returns a string object with the achieved score and grade

        Returns:
            str: Result text (score and grade)

        """
        self.__calculate_grade()
        # variable for the grade string
        grade_text = "\nGrade: " + self.__grade
        # variable for the __score string
        __score_text = "Your score was: " + str(self.__score) + "%."
        return __score_text + grade_text

    def __calculate_grade(self):
        """
        Calculates the grade based on the score achieved on this questionnaire
        """
        score = 0.0
        grade_dictionary = self.__xblock.grade_dictionary
        if self.__is_score_calculated is False:
            score = self.__calculate_score()
        # calculate the score in percent
        self.__score = (score / self.__total_score) * 100
        # due to confidence level, ensure that score cannot be higher then 100%
        if self.__score > 100:
            self.__score = 100
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
            | ``__get_current_question``: Returns the question data belonging to the passed question id
            | ``__check_if_answer_is_correct``: Checks if the submitted answers are the correct ones

        Returns:
            float: The total score achieved on this questionnaire

        """
        score = 0.0
        student_answer_dictionary = self.__xblock.student_answer_dictionary
        for answer, details in student_answer_dictionary.iteritems():
            # get question and confidence level
            question = self.__get_current_question(details['questionId'])
            confidence_level = self.__get_selected_confidence_level_score(details['confidence'])
            # check the selected answer(s) for this question and return score
            score += self.__check_if_answer_is_correct(details['chosen'], question, confidence_level)
        self.__is_score_calculated = True
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
        Returns the question data belonging to the passed question id.

        Arguments
            question_id (int): The id of the question to retrieve data from

        Returns:
            dict: Dictionary containing the data for this question id

        """
        counter = 0
        question = None
        question_not_found = True
        question_dictionary = self.__question_dictionary
        # loop until the question is found, or all questions are checked
        while question_not_found and counter < len(question_dictionary):
            if question_dictionary[counter]['id'] == question_id:
                question = question_dictionary[counter]
                question_not_found = False
            counter += 1
        return question

    @staticmethod
    def __check_if_answer_is_correct(chosen_answers, question, confidence_level):
        """
        Checks if the selected answer(s) on the current question are correct.

        This functions checks the submitted answers to see if they are correct.
        This is achieved by comparing the selected answers against the answers
        belonging to the question, to see which one(s) are correct. The score
        for each answer is based on the selected confidence level for this
        question.

        Arguments:
            chosen_answers (dict): The submitted answers for this question
            question (dict): The question which these answers belong to
            confidence_level (dict): The selected confidence level for this question

        Returns:
            float: The total score for this question

        """
        score = 0.0
        # loop through the submitted answers and those belonging to the question
        for current_answer in chosen_answers:
            for current_alternative in question['alternatives']:
                # if this is one of the submitted answers, check if it is correct
                if int(current_alternative['id']) == current_answer:
                    if current_alternative['isCorrect']:
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

    def check_if_dictionaries_is_set(self):
        """
        Checks if the dictionaries used have content (for debugging purposes)

        Returns:
             str: String stating whether or not the given dictionaries have content

        """
        # get the dictionaries
        questions_dictionary = self.__question_dictionary
        student_answers_dictionary = self.__xblock.student_answer_dictionary
        grade_dictionary = self.__xblock.grade_dictionary
        confidence_level_dictionary = self.__xblock.confidenceLevels
        # get and return the result
        result = self.__check_status_of_dictionary("Questions", questions_dictionary)
        result += self.__check_status_of_dictionary("SubmittedAnswers", student_answers_dictionary)
        result += self.__check_status_of_dictionary("Grades", grade_dictionary)
        result += self.__check_status_of_dictionary("Confidence Level", confidence_level_dictionary)
        return result

    def __check_status_of_dictionary(self, name, dictionary):
        """
        Checks if the passed dictionary is None (empty) or has content (for debugging purposes).

        Arguments:
            name (str): The name of this dictionary (for text output)
            dictionary (dict): The dictionary to check

        Returns:
             str: String informing whether or not the dictionary has content

        """
        result = self.__check_if_dictionary_has_content(dictionary)
        # check content of passed dictionary
        if result is None:
            status = "Dictionary (" + name + ") is None."
        else:
            status = "Dictionary (" + name + ") " + str(result)
        return status

    @staticmethod
    def __check_if_dictionary_has_content(dictionary):
        """
        Checks if the passed dictionary has content or if it is None.
        The function either returns None (if dictionary is empty) or
        a string with the content and the length of the dictionary.
        (for debugging purposes)

        Arguments:
            dictionary (dict): Dictionary to check

        Returns:
            object: None || String (str)

        """
        content = None
        if dictionary is not None:
            content = "Content: " + str(dictionary) + " \nLength: " + str(len(dictionary))
        return content

