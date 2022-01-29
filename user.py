import db
import analyze as ana


class User:

    def __init__(self, username):
        self._username = username

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    def __str__(self):
        return f"{self.username}"


class UserDB(User):

    def __init__(self, username, database=db.get_db()):
        User.__init__(self, username)
        self._best_habit = None
        self._worst_habit = None
        self._habit_list = None
        self._database = database

    # Getter- und Setter-Methoden
    @property
    def best_habit(self):
        return self._best_habit

    @best_habit.setter
    def best_habit(self, best_habit):
        self._best_habit = best_habit

    @property
    def worst_habit(self):
        return self._worst_habit

    @worst_habit.setter
    def worst_habit(self, worst_habit):
        self._worst_habit = worst_habit

    @property
    def habit_list(self):
        return self._habit_list

    @habit_list.setter
    def habit_list(self, habit_list):
        self._habit_list = habit_list

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    # eigentliche Klassenmethoden
    def store_user(self):
        db.add_user(self)

    def return_habit_list(self):
        self.habit_list = ana.habit_creator(self)
        return self.habit_list

    def determine_best_habit(self):
        longest_streak_of_all, best_habit = ana.calculate_longest_streak_of_all(self.habit_list)
        self.best_habit = best_habit  # ist möglicherweise auch eine Liste oder?
        return longest_streak_of_all, best_habit  # TODO: generell bei Klassenmethoden überlegen, ob ich die returns
        # brauche

    def determine_worst_habit(self):
        """the worst habit is the one with which the user struggled the most last month, i.e., the habit with the lowest
         completion rate (ein worst habit gibt es nur, wenn der Nutzer mindestens ein daily oder weekly habit hat)"""
        habits_with_data = ana.find_habits_with_data(self.return_habit_list())
        pass

    def analyze_habits(self, periodicity: str = None):
        pass
