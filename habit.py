import db
from datetime import date, datetime
import analyze as an


class Habit:
    def __init__(self, name, periodicity, user):
        self.__name = name
        self.__periodicity = periodicity
        self.__user = user
        self.__current_streak = 0  # TODO: Benötigen die drei hinzugefügten Attribute noch Getter und Setter-Methoden?
        self.__best_streak = 0
        self.__last_completion = None  # TODO: Überprüfen, ob noch notwendig

    # Setter # TODO: Entscheidung: braucht man Setter auch für User?
    def __setName(self, name):
        self.__name = name

    def __setPeriodicity(self, periodicity):
        self.__periodicity = periodicity

    def __set_last_completion(self, last_completion):
        self.__last_completion = last_completion

    # Getter
    def __getName(self):
        return self.__name

    def __getPeriodicity(self):
        return self.__periodicity

    def __getUser(self):
        return self.__user

    def __get_last_completion(self):
        return self.__last_completion

    # Definition der Properties
    name = property(__getName, __setName)
    periodicity = property(__getPeriodicity, __setPeriodicity)
    user = property(__getUser)
    last_completion = property(__get_last_completion, __set_last_completion)

    # Inkrementieren des Streaks
    def increment_streak(self):  # TODO: Überprüfen, ob noch notwendig
        self.__current_streak += 1

    # Einstellen des besten Streaks
    def determine_best_streak(self):
        if self.__current_streak > self.__best_streak:
            self.__best_streak = self.__current_streak
            # wenn ein hinzugefügtes check_date vor einem bereits hinzugefügten check liegt, dann kann das best streak
            # das auch nachträglich zum best streak werden, obwohl es niemals current streak war
            # am besten noch Funktion schreiben, die das letzte Ausführungsdatum zurückgibt und anhand dessen
            # den current streak berechnet
            # TODO: Funktion überarbeiten (siehe oben)


# TODO: def __str__(self) Funktion noch in die Habit-Klasse einbauen


class HabitDB(Habit):

    def store_habit(self, data_base, creation_time=None):
        db.add_habit(data_base, self, creation_time)

    def check_off_habit(self, data_base, check_date: str = None):
        """

        :param data_base:
        :param check_date:
        :type check_date: object
        """
        if not check_date:
            self.last_completion = str(date.today())
        elif not self.last_completion or date.fromisoformat(check_date) > date.fromisoformat(self.last_completion):
            # last_completion wird nur geändert, wenn das aktuelle Datum von Check-Date größer ist als das last
            # completion date oder es noch keins gibt
            self.last_completion = check_date
        db.add_period(data_base, self, check_date)

