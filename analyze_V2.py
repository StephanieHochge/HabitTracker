import pandas as pd
import db
from datetime import date, timedelta
import habit as hb
import dateutil.relativedelta
import collections


# TODO: vielleicht kann man die ganzen Funktionen, wo einfach nur Daten zurückgegeben werden in ein separates File
#  auslagern (außerhalb der Analyse, vielleicht in db?)
# create a pandas data fram from tables
def create_data_frame(database, table):
    """
    creates a pandas dataframe from database tables
    :param database: the database which contains the desired table
    :param table: the table to be created - either "Habit", "HabitAppUser" or "Period"
    :return: dataframe from the table
    """
    habit_columns = ["PKHabitID", "FKUserID", "Name", "Periodicity", "CreationTime"]
    # TODO: Überprüfen: Gibt es eine bessere Möglichkeit, die Table Header zu übergeben?
    user_columns = ["PKUserID", "UserName"]
    period_columns = ["PKPeriodID", "FKHabitID", "PeriodStart", "CompletionDate", "StreakName"]
    column_names = {"Habit": habit_columns, "HabitAppUser": user_columns, "Period": period_columns}
    sql_query = pd.read_sql_query(f'''SELECT * FROM {table}''', database)
    return pd.DataFrame(sql_query, columns=column_names[table])


# return the user_id of a user
def return_user_id(user):
    """
    returns the user_id of a user
    :param user: the user
    :return: the user's user_id
    """
    user_df = create_data_frame(user.database, "HabitAppUser")
    user_id = user_df.loc[user_df["UserName"] == user.username]
    return user_id.iloc[0, 0]


# checks if user name is already existing
def check_for_user(user):
    """
    checks if the entered user name is already existing
    :param user: the user
    :return: True if the user name already exists and false if not
    """
    user_df = create_data_frame(user.database, "HabitAppUser")
    users = list(user_df["UserName"])
    return True if user.username in users else False


# return the habits of a user with their periodicity
def return_user_habits(user):
    """
    :param user: the user
    :return: a pandas data frame containing the habits of the user and other data
    """
    user_id = return_user_id(user)
    habit_df = create_data_frame(user.database, "Habit")
    return habit_df.loc[habit_df["FKUserID"] == user_id]


# return the habit_id of a user's habit
def return_habit_id(habit):  # dieselbe Funktion gibt es auch schon für die Datenbank...
    """

    :param habit: the habit for which the ID is to be returned
    :return: the habit id (int)
    """
    user_habits = return_user_habits(habit.user)
    user_habit = user_habits.loc[user_habits["Name"] == habit.name]
    return user_habit.iloc[0, 0]


# return completions of a specific habit
def return_habit_completions(habit):
    """

    :param habit: the habit for which all completions are to be returned
    :return: a data frame containing all completions of the user's habit
    """
    habit_id = return_habit_id(habit)
    period_df = create_data_frame(habit.database, "Period")
    habit_data = period_df.loc[period_df["FKHabitID"] == habit_id]
    return habit_data["CompletionDate"].to_list()


# Return a list of all currently tracked habits of a user
def return_habits_only(user):
    """
    :param user: the user
    :return: a list containing only the habits of the user
    """
    defined_habits = return_user_habits(user)
    return defined_habits["Name"].to_list()


# return the periodicity of a habit.
def return_periodicity(habit):  # can be used to load habit
    user_habits = return_user_habits(habit.user)
    habit_data = user_habits.loc[user_habits["Name"] == habit.habit_name]
    periodicity_series = habit_data["Periodicity"]
    return periodicity_series.to_list()[0]


# Filter for periodicity and return habits with said periodicity
def return_habits_of_type(user, periodicity):
    """

    :param user: the user (object)
    :param periodicity: the periodicity for which the user looks (str)
    :return: a pandas series with the names of the user's habits of the specified periodicity
    """
    defined_habits = return_user_habits(user)
    habits_of_type = defined_habits.loc[defined_habits["Periodicity"] == periodicity]
    return habits_of_type["Name"]


# change a list of dates as strings into a list of dates as datetime objects
def to_date_format(check_dates):
    return list(map(lambda x: date.fromisoformat(x), check_dates))


def weekly_start(check_date):
    diff_to_start = timedelta(days=check_date.weekday())
    return check_date - diff_to_start


def monthly_start(check_date):
    diff_to_start = timedelta(days=check_date.day - 1)
    return check_date - diff_to_start


def yearly_start(check_date):
    return date.fromisoformat(f"{check_date.year}-01-01")


# calculate the period start for one completion only
def calculate_one_period_start(periodicity, check_date):
    date_as_list = [check_date]
    period_start = calculate_period_starts(periodicity, date_as_list)
    return period_start[0]


# calculate the period start for each completion in a list, return list of period starts
def calculate_period_starts(periodicity, check_dates):
    if isinstance(check_dates[0], str):  # wandelt das nur ins Datumsformat um, wenn es noch nicht in diesem ist
        check_dates = to_date_format(check_dates)
    period_start_funcs = {
        "daily": (lambda x: x),
        "weekly": weekly_start,
        "monthly": monthly_start,
        "yearly": yearly_start
    }
    period_start_func = period_start_funcs[periodicity]
    return list(map(period_start_func, check_dates))


# remove duplicates in the list and sort it
def tidy_starts(period_starts):
    return sorted(list(set(period_starts)))


# checks what time difference between two completions is allowed
def check_in_time(periodicity):
    timeliness = {"daily": timedelta(days=1),
                  "weekly": timedelta(days=7),
                  "monthly": timedelta(days=31),  # wenn ein Habit in einem Monat nicht durchgeführt wurde, ist das
                  # timedelta mind. 58 days
                  "yearly": timedelta(days=366)
                  }
    return timeliness[periodicity]


# add future period to list to correctly calculate streaks and breaks
def add_future_period(tidy_period_starts, periodicity):
    period_starts = tidy_period_starts  # notwendig, weil sonst die eigentliche Liste verändert wird
    duration = check_in_time(periodicity)  # ungefähre Dauer einer Periode
    future_period = calculate_one_period_start(periodicity, date.today() + 2*duration)  # Berechnung einer
    # zukünftigen Periode
    if period_starts[-1] != future_period:  # wenn die aktuelle Periode nicht in der aufgeräumten Liste enthalten ist,
        # wird sie hinzufügt zur Berechnung der Breaks
        period_starts.append(future_period)
    return period_starts


# calculate the difference of two consecutive elements in a list
def diffs_list_elements(period_starts):
    return [t - s for s, t in zip(period_starts, period_starts[1:])]


# prepare for streak and break analysis
# funktioniert
def return_period_starts_curr(habit):
    """

    :return: returns
    """
    check_dates = return_habit_completions(habit)
    period_starts = calculate_period_starts(habit.periodicity, check_dates)
    tidy_periods = tidy_starts(period_starts)
    return add_future_period(tidy_periods, habit.periodicity)


def check_current_period(period_starts_curr, periodicity):
    cur_period = calculate_one_period_start(periodicity, date.today())
    return True if cur_period in period_starts_curr else False


# funktioniert auch
def calculate_break_indices(period_starts_curr, periodicity):
    diffs = diffs_list_elements(period_starts_curr)
    in_time = check_in_time(periodicity)
    return [index for index, value in enumerate(diffs) if value > in_time]


# generate list of streak lengths of one habit
# funktioniert für die vier getesteten Habits
def calculate_streak_lengths(habit):
    # TODO: wird diese Funktion auch so verwendet? Wenn ja, dann get this to work for habits which have not been
    #  checked off yet
    period_starts_curr = return_period_starts_curr(habit)
    break_indices = calculate_break_indices(period_starts_curr, habit.periodicity)  # es muss immer break indices
    # geben, weil ja die zukünftige Periode hinzugefügt wird
    streak_lengths = [-1]  # weil der erste Streak sonst in der folgenden Berechnung nicht berücksichtigt wird
    streak_lengths[1:] = break_indices  # anhängen der restlichen Break Indizes
    return diffs_list_elements(streak_lengths)


# calculate the longest streak of one habit
def calculate_longest_streak(habit):
    check_dates = return_habit_completions(habit)  # kann schon null sein, wenn es keine completions gibt
    if not check_dates:
        return 0
    else:
        streak_lengths = calculate_streak_lengths(habit)
        return max(streak_lengths)


# create a list of the user's habits
def habit_creator(user):
    # TODO: Was passiert, wenn der User noch keine Habits angelegt hat?
    habit_list = return_habits_only(user)
    periodicities = return_user_habits(user)["Periodicity"].to_list()
    combined = list(zip(habit_list, periodicities))
    return list(map(lambda x: hb.HabitDB(x[0], x[1], user, user.database), combined))


def calculate_longest_streak_per_habit(habit_list):
    habit_names = [(habit.name, habit.periodicity) for habit in habit_list]  # funktioniert
    longest_streaks = map(calculate_longest_streak, habit_list)
    return dict(zip(habit_names, longest_streaks))


# calculate the longest streak of all habits
def calculate_longest_streak_of_all(habit_list):
    """
    the habit with the longest streak is defined as the habit which was performed the most periods in a row
    :return:
    """
    # TODO: Testen, was passiert, wenn mehrere Habits dieselbe Streak Length haben (müsste funktionieren)
    longest_streaks = calculate_longest_streak_per_habit(habit_list)
    if not longest_streaks:  # wenn noch kein Habit completed wurde
        return None, None
    else:
        longest_streak_of_all = longest_streaks[max(longest_streaks, key=longest_streaks.get)]
        best_habits = [key for (key, value) in longest_streaks.items() if value == longest_streak_of_all]  # it is
        # possible that two habits have the same streak lengths, this way they would both be returned
        return longest_streak_of_all, best_habits


# calculate the number of breaks within a list of dates
# funktioniert
def calculate_breaks(habit):
    """
    diese Funktion gibt die Anzahl an breaks aus
    :param habit:
    :return:
    """
    period_starts_curr = return_period_starts_curr(habit)
    break_indices = calculate_break_indices(period_starts_curr, habit.periodicity)
    if check_current_period(period_starts_curr, habit.periodicity):
        return len(break_indices) - 1  # wenn der Habit in der aktuellen Periode schon ausgeführt wurde, dann gibt es
        # eine Break weniger als break_indices ausrechnet (weil ja die zukünftige Periode mit berücksichtigt wird)
    else:
        return len(break_indices)

