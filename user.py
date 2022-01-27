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
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    # eigentliche Klassenmethoden
    def store_user(self):
        db.add_user(self)

    def calculate_best_habit(self):
        habit_list = ana.habit_creator(self)
        longest_streak_of_all, best_habits = ana.calculate_longest_streak_of_all(habit_list)
        return longest_streak_of_all, best_habits

    def analyze_habits(self, periodicity: str = None):
        pass
