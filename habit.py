import analyze as ana
import db


class Habit:
    """Every habit instance represents a user's habit, defined by a name, its periodicity and the user who
    created the habit.

    Attributes:
        name ('str'): the habit's name
        periodicity ('str'): the habit's periodicity (either daily, weekly, monthly, or yearly) defining the time
                            frame in which a user wants to complete a habit.
        user ('user.UserDB'): the user who created the habit
    """

    def __init__(self, name: str, periodicity: str, user):
        self.name = name
        self.periodicity = periodicity
        self.user = user

    def __str__(self):
        return f"{self.name} with {self.periodicity} periodicity"


class HabitDB(Habit):
    """This class is used to handle a habit's statistics as well as its data stored in the database. The HabitDB
    class is a subclass of Habit and therefore inherits the name, periodicity and user from Habit.

    Attributes:
        name ('str'): the habit's name
        periodicity ('str'): the habit's periodicity (either daily, weekly, monthly, or yearly) defining the time
                            frame in which a user wants to complete a habit.
        user ('user.UserDB'): the user who created the habit
        database (sqlite3.connection): the database connection which stores user data
    """

    def __init__(self, name: str, periodicity: str, user):
        Habit.__init__(self, name, periodicity, user)
        self.database = user.database

    @property
    def last_completion(self):
        """the date when the habit was last completed ('str', read-only)"""
        completions = ana.return_completions(self)
        return None if not completions else max(completions)

    @property
    def best_streak(self):
        """the habit's longest streak, i.e., the maximum number of periods in a row, in which the user
        has completed the habit ('int', read-only)"""
        return ana.calculate_longest_streak(self)

    @property
    def current_streak(self):
        """the habit's current streak, i.e., current number of periods in a row, in which the user has
        completed the habit (no completion in the current period is not counted as a break, as the user
        can still complete the habit in the current period) ('int', read-only)"""
        return ana.calculate_curr_streak(self)

    @property
    def breaks_total(self):
        """the number of breaks (i.e., streak interruptions) since the first habit completion (if
        more than one period has elapsed between two habit completions, this is counted as one break)
        ('int', read-only)"""
        return ana.calculate_break_no(self)

    @property
    def completion_rate(self):
        """the number of periods in the last 4 weeks (full weeks for weekly habits) in which the habit
        was completed divided by the total number of periods (only available for daily and weekly habits),
        multiplied by 100 and then rounded ('int', read-only)"""
        return round((ana.calculate_completion_rate(self))*100)

    def store_habit(self, creation_time=None):
        """store the habit in the database specified in the 'database' attribute"""
        db.add_habit(self, creation_time)

    def check_off_habit(self, check_date: str = None):
        """store a completion for the habit with the specified date.

        :param check_date: the date of the day, the habit was completed ('str'). If no date is provided, the
        current date is taken as the completion date.
        """
        db.add_completion(self, check_date)

    def delete_habit(self):
        """delete the habit and its data from the database"""
        db.delete_habit(self)

    def modify_habit(self, name: str = None, periodicity: str = None):
        """modify the habit's name, periodicity or both and store the modification in the database

        :param name: the habit's new name ('str', optional)
        :param periodicity: the habit's new periodicity ('str', optional)
        """
        db.modify_habit(self, name, periodicity)
        if periodicity:
            self.periodicity = periodicity
        if name:
            self.name = name

    def analyze_habit(self):
        """provide a detailed analysis of the habit's data: periodicity, last completion date, longest streak,
        current streak, total breaks, completion rate.

        :return: a list of the habit's statistics ('list')
        """
        data = [self.periodicity, self.last_completion, f"{self.best_streak} period(s)",
                f"{self.current_streak} period(s)", self.breaks_total]
        data.append(f"{self.completion_rate} %") if self.periodicity in ["daily", "weekly"] else data.append("---")
        return data

