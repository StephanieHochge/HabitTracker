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

    def __init__(self, username, database):
        User.__init__(self, username)
        self._best_habit = None
        self._worst_habit = None
        self._habits = None
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
    def habits(self):
        return self._habits

    @habits.setter
    def habits(self, habits):
        self._habits = habits

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

    def return_habit_information(self, periodicity=None):
        habit_info = ana.return_habit_info(self, periodicity)
        if not periodicity:
            habit_info = habit_info.sort_values("Periodicity")
        return habit_info.to_string(index=False)

    def determine_best_habit(self):
        habits_with_data = ana.find_completed_habits(self.return_habit_list())
        longest_streak_of_all, best_habit = ana.calculate_longest_streak_of_all(habits_with_data)
        self.best_habit = ", ".join(best_habit)  # trennt mehrere Habitnamen mit einem Komma
        return longest_streak_of_all  # TODO: generell bei Klassenmethoden überlegen, ob ich die returns
        # brauche

    def determine_worst_habit(self):
        """the worst habit is the one with which the user struggled the most last month, i.e., the habit with the lowest
         completion rate (ein worst habit gibt es nur, wenn der Nutzer mindestens ein daily oder weekly habit hat)"""
        habits_with_data = ana.find_completed_habits(self.return_habit_list())
        lowest_completion_rate, worst_habit = ana.calculate_worst_completion_rate_of_all(habits_with_data)
        self.worst_habit = ", ".join(worst_habit)
        return lowest_completion_rate

    def analyze_habits(self):
        # TODO: hier am besten noch anbieten, nur Habits einer bestimmten Periodizität zu analysieren
        analysis = ["Habit(s) with the longest streak: ", "longest streak of all: ",
                    "Habit(s) with the lowest completion rate (last 4 weeks): ",
                    "lowest completion rate of all: "]
        longest_streak = self.determine_best_habit()
        lowest_completion_rate = self.determine_worst_habit()
        data = [self.best_habit, f"{longest_streak} periods", self.worst_habit,
                f"{round((lowest_completion_rate*100))} %"]
        analysis_df = ana.list_to_df(analysis, data)
        habit_list = self.return_habit_list()
        habit_comparison = ana.analyse_all_habits(habit_list)
        return habit_comparison, analysis_df.to_string(index=False)
