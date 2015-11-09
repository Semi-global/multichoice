class CalculateGrade:

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
        grade_text = "Grade: "  # variable for the grade string
        __score_text = "\nYour __score was: "  # variable for the __score string
        return __score_text + str(self.__score) + grade_text + self.__grade

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

    def __calculate_score(self):
        """
        Calculates the score based on the submitted answers and selected confidence level.

        This function calculates the score for the questionnaire the student has submitted.
        It loops through all the submitted answers, retrieving both the selected answer and
        the selected confidence level for this answer. The confidence level is retrieved
        through the helper function ``get_selected_confidence_level_score``

        See:
            ``get_selected_confidence_level_score``

        Returns:
            float: The score achieved on this questionnaire

        """
        score = 0.0
        # get the students submitted answers and loop through them
        stud_answer_array = self.__xblock.student_answerArray
        for answer in stud_answer_array:
            confidence_level = self.__get_selected_confidence_level_score(answer.confidenceLevel)
            if answer.isCorrect:
                score += confidence_level["correct"]
            else:
                score += confidence_level["wrong"]
        return score

    def __get_selected_confidence_level_score(self, selected_confidence_level):
        """
        Returns a dictionary with score values for the current answer

        Arguments:
            selected_confidence_level (str): Confidence level for current answer

        Returns:
            dict: Score values for the current answer

        """
        confidence_level_dictionary = self.__xblock.confidenceLevels
        # get and return selected confidence level
        if selected_confidence_level in ["low", "Low", "LOW"]:
            return confidence_level_dictionary["low"]
        elif selected_confidence_level in ["normal", "Normal", "NORMAL"]:
            return confidence_level_dictionary["normal"]
        elif selected_confidence_level in ["high", "High", "HIGH"]:
            return confidence_level_dictionary["high"]
