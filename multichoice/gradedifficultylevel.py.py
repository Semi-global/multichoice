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

    def __init__(self, question_list=list, bonus_point=int):
        """
        Constructor for the class to grade submitted questionnaire with difficulty level

        Arguments:
            question_list (list): The list of questions in the given questionnaire
            bonus_point (list): The bonus points given to those that guessed/voted correctly

        """
        self.__bonus_point = bonus_point
        self.__question_list = question_list
        self.__rated_difficulty_list = list()
        self.__submitted_ratings_list = list()
        self.__dificulty_rating_list = list()
        self.__submitted_student_answers = list()  # __xblock.student_dictionary_answers

    def score_submitted_difficulty_levels(self):
        """
        For each submission, it is checked whether or not the given question
        contains a difficulty rating (e.g. above/below average). If it does,
        then for each student, it is counted up which one it was marked as.
        This is done for all questions with a difficulty level.

        Now that we have the difficulty rating, the one having the most guesses,
        gives the bonus point. E.g. if 6/10 found Q1 to be Above, then these 6
        gets the bonus points (added to the students original score).
        This is then done for each question with a difficulty rating.

        After completion, the list with updated score for each student is returned.

        Returns:
             list: List with updated scores for each student that guessed/voted correctly

        """
        students_difficulty_data = self.__create_list_of_student_difficulty_data()
        self.__submitted_student_answers = self.__update_students_score(students_difficulty_data)
        return self.__submitted_student_answers

    def __create_list_of_student_difficulty_data(self):
        """
        This functions loops through all the students and all their
        submitted answers on this questionnaire. For each answer that
        has a difficulty level, its data is stored in the list which is
        returned. Since this list will be large and have no sorting, its
        recommended to process input by using the function

        See:
            |  ```__sort_difficulty_levels_based_on_question```
            |  ```DifficultyLevel```
        Returns:
             list: List containing DifficultyLevel objects for each students submitted question

        """
        difficulty_rating_list = list()
        students_difficulty_data = list()
        submitted_student_answers = self.__submitted_student_answers
        # loop through all the students
        for student in submitted_student_answers:
                question_id = -1
                student_score = student.get_score()
                student_id = student.get_student_id()
                # loop through the submitted answers for this student
                for answer in student:
                    current_question_id = answer.get_question_id()
                    if answer.get_selected_difficuly_level() is not None \
                            and current_question_id != question_id:
                        question_id = current_question_id
                        difficulty_rating = answer.get_selected_difficuly_level()
                        difficulty_level_obj = DifficultyLevel(question_id, difficulty_rating, 0)
                        difficulty_rating_list.append(difficulty_level_obj)
                stud_diff_obj = StudentsDifficultyData(student_id, student_score, difficulty_rating_list)
                students_difficulty_data.append(stud_diff_obj)
        self.__rated_difficulty_list = self.__sort_difficulty_levels_based_on_question(difficulty_rating_list)
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
            processed_ratings = 0
            question_id = question.get_question_id()
            # comprehended list containing all difficulty ratings for this question
            question_rating_list = [rating for rating in difficulty_rating_list
                                    if rating.get_question_id() == question_id]
            # loop through the ratings for this question
            while counter < len(question_rating_list) and processed_ratings < len(question_rating_list):
                difficulty_level = question_rating_list[counter].get_difficulty_level()
                # is this a new difficulty rating for the current question?
                if temp_list is not None and difficulty_level not in temp_list:
                    # get all the votes for this difficulty
                    votes = len([rating for rating in difficulty_rating_list
                                 if rating.get_difficulty_level() == difficulty_level])
                    difficulty_level_obj = DifficultyLevel(question_id, difficulty_level, votes)
                    temp_list.append(difficulty_level)
                    rated_difficulty_list.append(difficulty_level_obj)
                counter += counter
        # return the updated list
        return rated_difficulty_list

    @staticmethod
    def __return_highest_voted_difficulty_level(question_id=int, difficulty_rating_list=list):
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
        # TODO: Add/update QuestionDifficultyData list here?
        votes = -1
        rating = None
        # get the difficulty ratings for the current question
        question_rating_list = [rating for rating in difficulty_rating_list
                                if rating.get_question_id() == question_id]
        # loop through the list to select the one with most votes
        for current_rating in question_rating_list:
            temp_votes = rating.get_votes()
            if temp_votes > votes:
                votes = temp_votes
                rating = current_rating.get_difficulty_level()
        return rating

    def __update_students_score(self, students_difficulty_data=list):
        """

        Arguments:
            students_difficulty_data (list):

        Returns:
             list:

        """
        # TODO: Write this function
        submitted_student_answers = self.__submitted_student_answers
        # loop here
        # update the list to the current data
        return submitted_student_answers

    def get_rated_difficulty_list(self):
        """
        Returns a list containing the total votes for each question
        submitted by the students. This is so the teacher can see
        which questions were deemed hard and easy.

        Returns:
             list: List containing the difficulty rating for each question

        """
        return self.__rated_difficulty_list

    def get_updated_list_of_students_score(self):
        """
        Returns a list containing the updated score for those students
        that guessed correctly on the difficulty level for the given questionnaire

        Returns:
             list: List containing the new score for the students

        """
        return self.__submitted_student_answers


class StudentsDifficultyData:
    __student_id = None
    __student_score = None

    def __init__(self, student_id=int, student_score=int, selected_difficulty_list=list):
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


class QuestionsDifficultyData:
    """
    Class container objectifying the questions that has a difficulty level.
    It contains the questions ID, the difficulty levels and which difficulty
    level that got most votes.
    """
    __question_id = None
    __selected_difficulty_level = None

    def __init__(self, question_id=int, selected_difficulty_level=str):
        self.__question_id = question_id
        self.__difficulty_score_list = list()
        self.__difficulty_rating_list = list()
        self.__selected_difficulty_level = selected_difficulty_level

    def get_question_id(self):
        """
        Returns the ID of this question

        Returns:
             int: Question ID

        """
        return self.__question_id

    def get_difficulty_rating_list(self):
        """
        Returns a list of difficulty levels belonging to this question

        Returns:
             list: Difficulty levels for this list

        """
        return self.__difficulty_rating_list

    def get_selected_difficulty_level(self):
        """
        Returns the difficulty level that most students guessed/voted for

        Returns:
             str: Most voted difficulty level

        """
        return self.__selected_difficulty_level


class DifficultyLevel:
    """
    Class container for the selected difficulty
    level and the number of votes it received.
    """
    __votes = None
    __question_id = None
    __difficulty_level = None

    def __init__(self, question_id=int, difficulty_level=str, votes=int):
        """
        Constructor for the difficulty level

        Arguments:
            question_id: ID of question this difficulty level belongs to
            difficulty_level: The description/name of this difficulty level
            votes: The number of votes for this difficulty level

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
        Update the number of votes for this difficulty level

        Arguments:
            vote (int): The number of votes for this difficulty level

        """
        self.__votes += vote



