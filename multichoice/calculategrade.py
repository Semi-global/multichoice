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

    def __init__(self, xblock, total_score):
        """
        Class constructor for score and grade calculation

        Initializes the class by setting variable values and calculating
        the students score and grade on the currently submitted questionnaire.

        Arguments:
             xblock (XBlock): Object of the parent XBlock class
            total_score (float): Score/points needed to achieve 100%

        """
        self.__xblock = xblock
        self.__total_score = total_score
        self.__is_score_calculated = False
        self.__calculate_grade()

    def __unicode__(self):
        """
        Returns a string object with the achieved score and grade

        Returns:
            str: Result text (score and grade)

        """
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
        # get the students submitted answers and loop through them
        student_answer_dictionary = self.__xblock.student_answers
        for answer, details in student_answer_dictionary.iteritems():
            # get question and confidence level
            question = self.__get_current_question(details['questionId'])
            confidence_level = self.__get_selected_confidence_level_score(details['confidence'])
            # check the selected answer(s) for this question and return score
            score += self.__check_if_answer_is_correct(details['chosen'], question, confidence_level)
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
        # loop until the question is found, or all questions are checked
        while question_not_found and counter < len(self.__xblock.questions):
            if self.__xblock.questions[counter]['id'] == question_id:
                question = self.__xblock.questions[counter]
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
