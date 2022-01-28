from datetime import datetime

import analyze as ana
import db


class Habit:
    def __init__(self, name, periodicity, user):  # TODO: eventuell für die Periodicity enum library verwenden
        self._name = name
        self._periodicity = periodicity
        self._user = user

    # Implementation der Getter– und Setter-Methoden mithilfe von @Property Decorators
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def periodicity(self):
        return self._periodicity

    @periodicity.setter
    def periodicity(self, periodicity):
        self._periodicity = periodicity

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user


class HabitDB(Habit):

    def __init__(self, name, periodicity, user, database=db.get_db()):
        Habit.__init__(self, name, periodicity, user)
        self._current_streak = 0
        self._best_streak = 0
        self._last_completion = None
        self._breaks_total = 0
        self._breaks_last_month = 0
        self._database = database

    # Getter und Setter Methoden mithilfe des @property decorators
    @property
    def current_streak(self):
        return self._current_streak

    @current_streak.setter
    def current_streak(self, current_streak):
        self._current_streak = current_streak

    @property
    def best_streak(self):
        return self._best_streak

    @best_streak.setter
    def best_streak(self, best_streak):
        self._best_streak = best_streak

    @property
    def last_completion(self):
        return self._last_completion

    @last_completion.setter
    def last_completion(self, last_completion):
        self._last_completion = last_completion

    @property
    def breaks_total(self):
        return self._breaks_total

    @breaks_total.setter
    def breaks_total(self, breaks_total):
        self._breaks_total = breaks_total

    @property
    def breaks_last_month(self):
        return self._breaks_last_month

    @breaks_last_month.setter
    def breaks_last_month(self, breaks_last_month):
        self._breaks_last_month = breaks_last_month

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    def __str__(self):
        return f"{self.name} with {self.periodicity} periodicity from {self.user} saved in {self.database}"

    # TODO: def __str__(self) Funktion noch in die Habit-Klasse einbauen

    # die übrigen Methoden
    def store_habit(self, creation_time=None):
        db.add_habit(self, creation_time)
        return True  # TODO: Chris fragen, ob das so gemeint war

    def check_off_habit(self, check_date: str = None):
        """

        :param check_date:
        :type check_date: object
        """
        if not check_date:
            self.last_completion = str(datetime.now())
        elif not self.last_completion or datetime.fromisoformat(check_date) > \
                datetime.fromisoformat(self.last_completion):
            # last_completion wird nur geändert, wenn das aktuelle Datum von Check-Date größer ist als das last
            # completion date oder es noch keins gibt
            self.last_completion = check_date
        db.add_completion(self, check_date)
        return True

    def find_last_check(self):
        completions = ana.return_habit_completions(self)
        if not completions:
            self.last_completion = None
        else:
            self.last_completion = max(completions)
        return self.last_completion

    def delete_habit(self):
        db.delete_habit(self)
        return True

    def modify_habit(self, name=None, periodicity=None):
        db.modify_habit(self, name, periodicity)
        if periodicity:
            self.periodicity = periodicity
        if name:
            self.name = name
        return True

    def calculate_best_streak(self):
        self.best_streak = ana.calculate_longest_streak(self)
        return self.best_streak

    def calculate_current_streak(self):
        self.current_streak = ana.calculate_curr_streak(self)
        return self.current_streak

    def calculate_breaks(self, last_month: bool = False):
        if last_month:
            self._breaks_last_month = ana.calculate_breaks(self)
            return self.breaks_last_month
        else:
            self.breaks_total = ana.calculate_breaks(self)
            return self.breaks_total

    def analyze_habit(self):
        self.calculate_breaks()
        self.calculate_best_streak()
        self.calculate_current_streak()
        self.find_last_check()
        analysis = ["periodicity: ", "last completion: ", "longest streak: ", "current streak: ", "breaks total: "]
        data = [self.periodicity, self.last_completion, f"{self.best_streak} periods",
                f"{self.current_streak} periods", self.breaks_total]
        if self.periodicity in ["daily", "weekly"]:
            self.calculate_breaks(last_month=True)
            analysis.append("breaks last month: ")
            data.append(self.breaks_last_month)
        return ana.list_to_df(analysis, data)

