_author_ = "Knut Lucas Andersen"


class GradeDifficultyLevel:
    """
    Class which updates the students score based on the submitted answers.
    A pre-requisite for getting a updated score is that at least one question
    contains a difficulty level scoring, and that the sum total of score/guesses
    for the given question is the same as the rest of the class.

    Furthermore, the class has been written in such a way that it is not locked
    to a given set of difficulty levels, meaning a question can have 2 or more,
    but the O(n) increases noticeable for a higher amount, since lists are used.

    Example:
        For a given Question, 6/10 say that this question is 'Above Average' in
        difficulty. This means that those 6 who voted for it to be 'Above' will
        get a bonus point. The bonus point score is based on the passed value
        in the constructor, making it changeable for each questionnaire.
    """

    __xblock = None
    __bonus_point = None

    def __init__(self, xblock, question_list=list, bonus_point=float):
        """
        Constructor for the class to grade submitted questionnaire with difficulty level

        Arguments:
            question_list (list): List containing objects of the class ```Question``` for this questionnaire
            bonus_point (float): The bonus points given to those that guessed/voted correctly

        See:
            ```Question```

        """
        self.__xblock = xblock
        self.__bonus_point = bonus_point
        self.__question_list = question_list
        self.__difficulty_rating_list = list()
        # TODO: Maybe pass just like question_list
        self.__submitted_student_answers = self.__xblock.submitted_student_answers

    def update_score_based_on_submitted_difficulty_levels(self):
        """
        For each submission, it is checked whether or not the given question
        contains a difficulty rating (e.g. Above/Below average). If it does,
        then for each student, it is counted up which one it was marked as.
        This is done for all questions with a difficulty level.

        Now that we have the difficulty rating, the one having the most guesses,
        gives the bonus point. E.g. if 6/10 found Q1 to be 'Above', then these 6
        gets the bonus points (added to the students original score).
        This is then done for each question with a difficulty rating.

        See:
            |  ```__create_list_of_student_difficulty_data```
            |  ```DifficultyLevel```
            |  ```StudentsDifficultyData```

        """
        bonus_point = self.__bonus_point
        # this must be called first, since it fills up self.__difficulty_rating_list

        students_difficulty_data_list = self.__create_list_of_students_difficulty_data()
        max_size = len(students_difficulty_data_list)
        rated_difficulty_list = self.__difficulty_rating_list
        # loop through all the students
        for index in range(0, max_size):
            achieved_bonus_points = 0
            student = students_difficulty_data_list[index]
            # loop through the submitted difficulty levels for this student
            for difficulty_level in student.get_difficulty_level_list():
                question_id = difficulty_level.get_question_id()
                selected_difficulty_level = difficulty_level.get_difficulty_level()
                highest_voted = self.__return_highest_voted_difficulty_level(question_id, rated_difficulty_list)
                # was this the guessed difficulty level
                if selected_difficulty_level == highest_voted:
                    achieved_bonus_points += bonus_point
            # update score in list and update index for next student
            students_difficulty_data_list[index].set_student_score(achieved_bonus_points)
        self.__submitted_student_answers = students_difficulty_data_list

    def __create_list_of_students_difficulty_data(self):
        """
        This functions loops through all the students and all their
        submitted answers for this questionnaire. For each answer that
        has a difficulty level, its data is stored in the list which is
        returned. Since this list will be large and have no sorting, its
        recommended to process input by using the function
        ```__sort_difficulty_levels_based_on_question```

        See:
            |  ```__sort_difficulty_levels_based_on_question```
            |  ```DifficultyLevel```
            |  ```StudentsDifficultyData```
        Returns:
             list: List of StudentsDifficultyData objects

        """
        # TODO: IF the current dummy data setup is re-used, parts of this function will be redundant!
        difficulty_rating_list = list()
        students_difficulty_data = list()
        submitted_student_answers = self.__submitted_student_answers
        # loop through all the students
        for student in submitted_student_answers:
            question_id = -1
            temp_rating_list = list()
            student_id = student.get_student_id()
            student_score = student.get_student_score()
            selected_difficulties_list = student.get_difficulty_level_list()
            # loop through the submitted difficulty selections for this student
            for selected_difficulty in selected_difficulties_list:
                current_question_id = selected_difficulty.get_question_id()
                difficulty_level = selected_difficulty.get_difficulty_level()
                if difficulty_level is not None and current_question_id != question_id:
                    question_id = current_question_id
                    difficulty_level_obj = DifficultyLevel(question_id, difficulty_level, 0)
                    temp_rating_list.append(difficulty_level_obj)
                    difficulty_rating_list.append(difficulty_level_obj)
            # TODO: These two lines may be redundant
            stud_diff_obj = StudentsDifficultyData(student_id, student_score, temp_rating_list)
            students_difficulty_data.append(stud_diff_obj)
        self.__difficulty_rating_list = self.__sort_difficulty_levels_based_on_question(difficulty_rating_list)
        return students_difficulty_data

    def __sort_difficulty_levels_based_on_question(self, difficulty_rating_list=list):
        """
        Since the function ```__create_list_of_student_difficulty_data``` is such a quick
        and dirty function, a clean up is needed. This is what this function does. It loops
        through each question and adds the difficulty level data for this. By using list
        comprehension, the list of difficulty ratings are filtered, so we only get the
        data for the given question. To further speed up and reduce time spent, this list
        is then looped through, where difficulty level is selected only once. This is
        achieved again by use of list comprehension, selecting only those that match
        the currently selected difficulty level and adding the total number of votes/guesses
        to a new list.

        This list contains elements equal to dr_count * q_count, because it has for each question
        an object listing the votes for that difficulty level on that question.

        Arguments:
            difficulty_rating_list (list): List containing objects of the class DifficultyLevel

        See:
            |  ```__create_list_of_student_difficulty_data```
            |  ```DifficultyLevel```

        Returns:
             list: List containing sorted DifficultyLevel objects for each question

        """
        rated_difficulty_list = list()
        question_list = self.__question_list
        for question in question_list:
            counter = 0
            temp_list = list()
            question_id = question.get_question_id()
            # comprehended list containing all difficulty ratings for this question
            question_rating_list = [rating for rating in difficulty_rating_list
                                    if rating.get_question_id() == question_id]
            max_size = len(question_rating_list)
            # loop through the ratings for the current question
            while counter < max_size:
                difficulty_level = question_rating_list[counter].get_difficulty_level()
                # is this a new difficulty rating for the current question?
                if temp_list is not None and difficulty_level not in temp_list:
                    # get all the votes for this difficulty
                    votes = len([rating for rating in question_rating_list
                                 if rating.get_difficulty_level() == difficulty_level])
                    difficulty_level_obj = DifficultyLevel(question_id, difficulty_level, votes)
                    temp_list.append(difficulty_level)
                    rated_difficulty_list.append(difficulty_level_obj)
                counter += 1
        # return the processed list
        return rated_difficulty_list

    @staticmethod
    def __return_highest_voted_difficulty_level(question_id=int, difficulty_rating_list=list()):
        """
        Retrieves a list of difficulty ratings for this question, and
        loops through it to find which difficulty level got the most
        votes. The name of this difficulty level is then returned.

        Arguments:
            question_id: The ID of the current question to score students on
            difficulty_rating_list (list): List of DifficultyLevel objects

        Returns:
            str: Highest voted difficulty level

        """
        votes = -1
        rating = None
        # get the difficulty ratings for the current question
        question_rating_list = [rating for rating in difficulty_rating_list
                                if rating.get_question_id() == question_id]
        # loop through the list to select the one with most votes
        for current_rating in question_rating_list:
            temp_votes = current_rating.get_votes()
            if temp_votes > votes:
                votes = temp_votes
                rating = current_rating.get_difficulty_level()
        return rating

    def get_difficulty_rating_list(self):
        """
        Returns a list of objects (DifficultyLevel) for the current questionnaire.
        Usage: Retrieve question, votes and difficulty level

        See:
            ```DifficultyLevel```

        Returns:
             list: List of DifficultyLevel objects

        """
        return self.__difficulty_rating_list

    def get_updated_list_of_students_score(self):
        """
        Returns a list of objects (StudentsDifficultyData) for the current questionnaire.
        Usage: Retrieve student, score and selected difficulty levels

        See:
            ```StudentsDifficultyData```

        Returns:
             list: List of StudentsDifficultyData objects

        """
        return self.__submitted_student_answers

    def print_students_updated_score(self):
        """
        Returns a string containing the selected difficulty level for each
        student; for each submitted question. It also shows the new score
        for the student.

        Returns:
            str: String with Student ID, submitted questions and new score

        """
        student_results = ''
        prev_question_id = -1
        for student in self.__submitted_student_answers:
            student_results += "<p>"
            student_results += "Student (ID: " + str(student.get_student_id())
            student_results += ") guessed the following: <br />"
            for difficulty_level in student.get_difficulty_level_list():
                question_id = difficulty_level.get_question_id()
                # we only want the question printed once
                if question_id != prev_question_id:
                    prev_question_id = question_id
                    student_results += "Q" + str(difficulty_level.get_question_id()) + ": "
                    student_results += difficulty_level.get_difficulty_level() + "<br />"
            student_results += "New score: " + str(student.get_student_score()) + "</p>"
        return student_results

    def print_difficulty_rating_votes(self):
        """
        Returns a string containing each question with their difficulty levels and their votes.

        Returns:
            str: The votes for each Questions difficulty level

        """
        prev_question_id = -1
        difficulty_statistics = ''
        # loop through all the difficulty level votes
        for difficulty_rating in self.__difficulty_rating_list:
            question_id = difficulty_rating.get_question_id()
            # we only want the question printed once
            if question_id != prev_question_id:
                # add newline separation if this is not the first question printed
                difficulty_statistics += ("<br />" if (prev_question_id > -1) else "")
                prev_question_id = question_id
                difficulty_statistics += "Question " + str(difficulty_rating.get_question_id())
                difficulty_statistics += " got the following votes: <br />"
            # print the difficulty level and the votes it got
            difficulty_statistics += "- " + difficulty_rating.get_difficulty_level() + " "
            difficulty_statistics += "(" + str(difficulty_rating.get_votes()) + ") <br />"
        return difficulty_statistics


class StudentsDifficultyData:
    __student_id = None
    __student_score = None

    def __init__(self, student_id=int, student_score=float, selected_difficulty_list=list):
        """
        Constructor for the Student to check the submitted difficulty levels

        Arguments:
            student_id (int): The Students ID
            student_score (float): The students current score
            selected_difficulty_list (list): List of objects for this student selected difficulty levels
                (based on the class DifficultyLevels)

        See:
            ```DifficultyLevels```

        """
        self.__student_id = student_id
        self.__student_score = student_score
        self.__selected_difficulty_list = selected_difficulty_list

    def get_student_id(self):
        """
        Returns the ID of this student

        Returns:
             int: Student ID

        """
        return self.__student_id

    def get_student_score(self):
        """
        Returns the score for this student

        Returns:
             float: Student score

        """
        return self.__student_score

    def get_difficulty_level_list(self):
        """
        Returns a list containing the submitted ```DifficultyLevel``` objects for this student

        Returns:
             list: List containing DifficultyLevel objects

        """
        return self.__selected_difficulty_list

    def set_student_score(self, score):
        """
        Adds the passed score to the total score for this student

        Arguments:
            score (float): The score to add for this student

        """
        self.__student_score += score


class DifficultyLevel:
    """
    Class creating objects of the available difficulty levels
    for the currently active questionnaire
    """
    __votes = None
    __question_id = None
    __difficulty_level = None

    def __init__(self, question_id=int, difficulty_level=str, votes=int):
        """
        Constructor for the difficulty level

        Arguments:
            question_id (int): ID of question this difficulty level belongs to
            difficulty_level (str): The description/name of this difficulty level
            votes (int): The number of votes for this difficulty level

        """
        self.__votes = votes
        self.__question_id = question_id
        self.__difficulty_level = difficulty_level

    def get_votes(self):
        """
        Returns the number of votes for this difficulty level

        Returns:
            int: Votes for this difficulty level

        """
        return self.__votes

    def get_question_id(self):
        """
        Returns the ID of the Question this difficulty level belongs to

        Returns:
            int: Question ID

        """
        return self.__question_id

    def get_difficulty_level(self):
        """
        Returns the name/description of this difficulty level

        Returns:
            str: Difficulty level name/description

        """
        return self.__difficulty_level

    def set_votes(self, vote):
        """
        Adds the passed value to this difficulty levels vote count

        Arguments:
            vote (int): The number of votes to add for this difficulty level

        """
        self.__votes += vote



