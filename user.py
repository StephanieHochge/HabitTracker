import db
import analyze as ana


class User:
    """Every user instance represents one user of the application.

    Attributes:
        username (str): the name of the user.
    """

    def __init__(self, username):
        self.username = username

    def __str__(self):
        return f"{self.username}"


class UserDB(User):
    """This class is used to handle the application's users, as well as their data stored in the database. The UserDB
    class is a subclass of User and therefore inherits the username from the User class.

    Attributes:
        all_habits (habit.HabitDB): a list of the user's tracked habits
        best_habit (str): the user's best habit(s), i.e., the name(s) of the habit(s), that has/have the longest
                        streak of all habits
        worst_habit (str): the user's worst habit(s), i.e., the name

    """

    def __init__(self, username, database):
        User.__init__(self, username)
        self.best_habit = None
        self.worst_habit = None
        self.database = database

    def store_user(self):
        db.add_user(self)

    def return_habits(self):
        return ana.habit_creator(self)

    def find_completed_habits(self):
        return ana.find_completed_habits(self.return_habits())

    def return_habit_information(self, periodicity=None):
        habit_info = ana.return_habit_info(self, periodicity)
        if not periodicity:
            habit_info = habit_info.sort_values("Periodicity")
        return habit_info.to_string(index=False)

    def determine_longest_streak(self):
        longest_streak_of_all, best_habit = ana.calculate_longest_streak_of_all(self.find_completed_habits())
        self.best_habit = ", ".join(best_habit)  # separate several habit names with a comma
        return longest_streak_of_all  # TODO: generell bei Klassenmethoden überlegen, ob ich die returns
        # brauche

    def determine_lowest_completion_rate(self):
        """the worst habit is the one with which the user struggled the most last month, i.e., the habit with the lowest
         completion rate (ein worst habit gibt es nur, wenn der Nutzer mindestens ein daily oder weekly habit hat)"""
        lowest_completion_rate, worst_habit = ana.calculate_worst_completion_rate_of_all(self.find_completed_habits())
        self.worst_habit = ", ".join(worst_habit)
        return lowest_completion_rate

    def analyze_habits(self):
        analysis = ["Habit(s) with the longest streak: ", "longest streak of all: ",
                    "Habit(s) with the lowest completion rate (last 4 weeks): ",
                    "lowest completion rate of all: "]
        longest_streak = self.determine_longest_streak()
        lowest_completion_rate = self.determine_lowest_completion_rate()
        data = [self.best_habit, f"{longest_streak} periods", self.worst_habit,
                f"{round((lowest_completion_rate*100))} %"]
        analysis_df = ana.list_to_df(analysis, data)
        habit_comparison = ana.analyse_all_habits(self.return_habits())
        return habit_comparison, analysis_df.to_string(index=False)
