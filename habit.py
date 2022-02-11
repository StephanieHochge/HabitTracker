from datetime import datetime, date

import analyze as ana
import db


class Habit:
    def __init__(self, name, periodicity, user):
        self.name = name
        self.periodicity = periodicity
        self.user = user


class HabitDB(Habit):

    def __init__(self, name, periodicity, user, database):
        Habit.__init__(self, name, periodicity, user)
        self.database = database

    def __str__(self):
        return f"{self.name} with {self.periodicity} periodicity from {self.user} saved in {self.database}"

    # die übrigen Methoden
    def store_habit(self, creation_time=None):
        db.add_habit(self, creation_time)

    def check_off_habit(self, check_date: str = None):
        """

        :param check_date:
        :type check_date: object
        """
        db.add_completion(self, check_date)

    @property
    def last_completion(self):
        completions = ana.return_completions(self)
        return None if not completions else max(completions)

    def delete_habit(self):
        db.delete_habit(self)

    def modify_habit(self, name=None, periodicity=None):
        db.modify_habit(self, name, periodicity)
        if periodicity:
            self.periodicity = periodicity
        if name:
            self.name = name

    @property
    def best_streak(self):
        return ana.calculate_longest_streak(self)

    @property
    def current_streak(self):
        return ana.calculate_curr_streak(self)

    @property
    def breaks_total(self):
        return ana.calculate_break_no(self)

    @property
    def completion_rate(self):
        return round((ana.calculate_completion_rate(self))*100)

    def analyze_habit(self):
        data = [self.periodicity, self.last_completion, f"{self.best_streak} period(s)",
                f"{self.current_streak} period(s)", self.breaks_total]
        data.append(f"{self.completion_rate} %") if self.periodicity in ["daily", "weekly"] else data.append("---")
        return data

