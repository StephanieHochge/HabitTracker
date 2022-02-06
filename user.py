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

    def return_habit_information(self):
        habit_info_df = ana.return_user_habits(self)[["Name", "Periodicity", "CreationTime"]]
        sorted_habits = habit_info_df.sort_values("Periodicity")
        return sorted_habits.to_string(index=False)

    def return_habits_of_type(self, periodicity):
        habits_of_type = ana.return_habits_of_type(self, periodicity)
        return habits_of_type.to_string(index=False)

    def determine_best_habit(self):
        habits_with_data = ana.find_habits_with_data(self.return_habit_list())
        longest_streak_of_all, best_habit = ana.calculate_longest_streak_of_all(habits_with_data)
        self.best_habit = ", ".join(best_habit)  # trennt mehrere Habitnamen mit einem Komma
        return longest_streak_of_all  # TODO: generell bei Klassenmethoden überlegen, ob ich die returns
        # brauche

    def determine_worst_habit(self):
        """the worst habit is the one with which the user struggled the most last month, i.e., the habit with the lowest
         completion rate (ein worst habit gibt es nur, wenn der Nutzer mindestens ein daily oder weekly habit hat)"""
        habits_with_data = ana.find_habits_with_data(self.return_habit_list())
        lowest_completion_rate, worst_habit = ana.calculate_worst_completion_rate_of_all(habits_with_data)
        self.worst_habit = ", ".join(worst_habit)
        return lowest_completion_rate

    def analyze_habits(self):
        # TODO: hier am besten noch anbieten, nur Habits einer bestimmten Periodizität zu analysieren
        analysis = ["Habit(s) with the longest streak: ", "longest streak of all habits: ",
                    "Habit(s) with the lowest completion rate during the last four weeks: ",
                    "lowest completion rate of all habits: "]
        longest_streak = self.determine_best_habit()
        lowest_completion_rate = self.determine_worst_habit()
        data = [self.best_habit, f"{longest_streak} periods", self.worst_habit, f"{round(lowest_completion_rate)} %"]
        analysis_df = ana.list_to_df(analysis, data)
        habit_list = self.return_habit_list()
        habit_comparison = ana.detailed_analysis_of_all_habits(habit_list)
        return  habit_comparison, analysis_df.to_string(index=False)
