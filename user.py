import db
import analyze as ana


class User:
    """Every user instance represents one user of the application.

    Attributes:
        username ('str'): the name of the user
    """

    def __init__(self, username: str):
        self.username = username

    def __str__(self):
        return f"{self.username}"


class UserDB(User):
    """This class is used to handle a user's statistics as well as their data stored in the database. The UserDB
    class is a subclass of User and therefore inherits the username from User.

    Attributes:
        username ('str'): the name of the user
        database ('sqlite3.connection'): the database connection which stores user data
    """

    def __init__(self, username: str, database):
        User.__init__(self, username)
        self.database = database

    @property
    def defined_habits(self):
        """a list of all the habits ('habit.HabitDB') that the user has created ('list', read-only)"""
        return ana.habit_creator(self)

    @property
    def habit_names(self):
        """a list containing the names ('str') of the user's defined habits ('list', read-only)"""
        return [habit.name for habit in self.defined_habits]

    @property
    def completed_habits(self):
        """a list of the user's habits ('habit.HabitDB') that have been completed at least once ('list', read-only)"""
        return ana.find_completed_habits(self.defined_habits)

    @property
    def longest_streak(self):
        """the value of the longest streak of all habits, i.e., the maximum number of consecutive periods in a row
        that a user has completed a habits ('int', read-only)"""
        longest_streak, _ = ana.calculate_longest_streak_of_all(self.completed_habits)
        return longest_streak

    @property
    def best_habit(self):
        """the best habit is defined as the habit(s) with the longest streak, i.e., the habit(s) that have been
        completed the most periods in a row ('str', read-only)"""
        _, best_habit = ana.calculate_longest_streak_of_all(self.completed_habits)
        best_habit = ", ".join(best_habit)  # separate several habit names with a comma
        return best_habit

    @property
    def lowest_completion_rate(self):
        """the value of the lowest completion rate of all habits. The completion rate is defined as
        the percentage of time periods in the last four weeks (full weeks for weekly habits) in which the
        habit was completed at least once."""
        user_periodicities = ana.return_ordered_periodicities(self)
        if "daily" in user_periodicities or "weekly" in user_periodicities:  # the completion rate is only calculated
            # for daily and weekly habits
            lowest_completion_rate, _ = ana.calculate_worst_completion_rate_of_all(self.completed_habits)
            return round((lowest_completion_rate*100))
        else:
            return "---"

    @property
    def worst_habit(self):
        """the worst habit is the daily or weekly habit with which the user struggled the most last month, i.e.,
        the habit with the lowest completion rate ('str', read-only)"""
        if self.lowest_completion_rate == "---":  # the completion rate is only calculated for daily and weekly habits
            return "---"
        else:
            _, worst_habit = ana.calculate_worst_completion_rate_of_all(self.completed_habits)
            worst_habit = ", ".join(worst_habit)
            return worst_habit

    def store_user(self):
        """store the user in the database specified in the 'database' attribute"""
        db.add_user(self)

    def return_habit_information(self, periodicity: str = None):
        """return the name, periodicity and creation time of either all of the user's habits (periodicity = None) or
        only the habits with a certain periodicity (e.g., periodicity = 'daily').

        :param periodicity: the periodicity for which information is to be returned ('str', optional)
        :return: a data frame containing the name, periodicity and creation time of the desired habits
        ('pandas.core.frame.DataFrame')
        """
        habit_info = ana.return_habit_info(self, periodicity)
        if not periodicity:
            habit_info = habit_info.sort_values("Periodicity")
        return habit_info

    def analyze_habits(self):
        """return an analysis of the user's habits. The analysis consists of summary statistics (the user's
        best habit(s), longest streak, worst habit(s) and lowest completion rate), as well as a detailed analysis
        of each habit (periodicity, last completion, longest streak, current streak, total breaks, completion
        rate).

        :return: a tuple ('tuple') containing the summary statistics ('pandas.core.frame.DataFrame') as well
        as the detailed analysis of each habit ('pandas.core.frame.DataFrame')
        """
        analysis = ["Habit(s) with the longest streak: ", "longest streak of all: ",
                    "Habit(s) with the lowest completion rate (last 4 weeks): ",
                    "lowest completion rate of all: "]
        data = [self.best_habit, f"{self.longest_streak} period(s)", self.worst_habit,
                f"{self.lowest_completion_rate} %"]
        analysis_df = ana.list_to_df(analysis, data)
        habit_comparison = ana.analyze_all_habits(self.defined_habits)
        return habit_comparison, analysis_df
