import pandas as pd
import db
from datetime import date, timedelta
import dateutil.relativedelta
import collections


# Create a pandas dataframe from database tables
def create_data_frame(data_base, table):
    """
    creates a pandas dataframe from database tables
    :param data_base: the database which contains the desired table
    :param table: the table to be created - either "Habit", "HabitAppUser" or "Period"
    :return: dataframe from the table
    """
    habit_columns = ["PKHabitID", "FKUserID", "Name", "Periodicity", "CreationTime"]
    # TODO: Überprüfen: Gibt es eine bessere Möglichkeit, die Table Header zu übergeben?
    user_columns = ["PKUserID", "UserName"]
    period_columns = ["PKPeriodID", "FKHabitID", "PeriodStart", "CompletionDate", "StreakName"]
    column_names = {"Habit": habit_columns, "HabitAppUser": user_columns, "Period": period_columns}
    sql_query = pd.read_sql_query(f'''SELECT * FROM {table}''', data_base)
    return pd.DataFrame(sql_query, columns=column_names[table])


# return all data of a specific habit
def return_habit_completions():
    pass


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
    if isinstance(check_dates[0], str):
        check_dates = to_date_format(check_dates)
    if periodicity == "daily":
        period_start_func = lambda x: x  # warum ist das grün unterkringelt?!
    elif periodicity == "weekly":
        period_start_func = weekly_start
    elif periodicity == "monthly":
        period_start_func = monthly_start
    else:  # periodicity == "yearly"
        period_start_func = yearly_start  # könnte man das Ganze nicht auch mit einem Dictionary machen?
    return list(map(period_start_func, check_dates))


# remove duplicates in the list and sort it
def tidy_starts(period_starts):
    return sorted(list(set(period_starts)))


# checks whether time difference is allowed
def check_in_time(periodicity):
    timeliness = {"daily": timedelta(days=1),
                  "weekly": timedelta(days=7),
                  "monthly": timedelta(days=31),  # wenn ein Habit in einem Monat nicht durchgeführt wurde, ist das
                  # timedelta mind. 58 days
                  "yearly": timedelta(days=366)
                  }
    return timeliness[periodicity]


# generate list of streak names
def streak_names(tidy_periods, periodicity):
    # TODO: check whether this also works for habits when they have not been checked off yet
    streaks = [1]
    diffs = [t - s for s, t in zip(tidy_periods, tidy_periods[1:])]
    in_time = check_in_time(periodicity)
    for count, value in enumerate(tidy_periods[1:]):  # skips the first element, as the first element of
        # the list has already been added
        if diffs[count] <= in_time:
            streaks.append(streaks[-1])
        else:
            streaks.append(streaks[-1]+1)
    return streaks


# zip list of streak names together with list of period_starts and create a data_frame
def calculate_longest_streak(streaks):
    streak_durations = collections.Counter(streaks)
    # hier auch bedenken, dass es mehrere Streaks mit der gleichen Länge geben kann
    streak_name = max(streak_durations, key=streak_durations.get)
    longest_streak = streak_durations[streak_name]
    list_of_keys = [key for (key, value) in streak_durations.items() if value == longest_streak]
    return longest_streak, list_of_keys  # die erste Zahl ist der longest streak, die zweite Liste sind die keys des
    # longest streak
    # diese Keys könnten verwendet werden, um die zugehörigen Daten rauszufinden


# get the len of each streak list, returns a list of the lengths
def get_streak_length():
    pass


# find the maximum length
def find_longest_streak():
    pass


# calculate the number of breaks within a list of dates
def calculate_breaks(periodicity, tidy_period_starts):
    """
    diese Funktion zählt die Breaks immer ab dem ersten Mal, an dem das Habit ausgeführt wurde, wenn der Habit in der
    letzten Periode ausgeführt wurde, aber noch nicht in der aktuellen Periode, wird dies nicht als Break gewertet
    :param periodicity:
    :param tidy_period_starts:
    :return:
    """
    period_starts = tidy_period_starts
    cur_period = calculate_one_period_start("yearly", date.today())  # Berechnung der aktuellen Periode
    if period_starts[-1] != cur_period:  # wenn die aktuelle Periode nicht in der aufgeräumten Liste enthalten ist,
        # wird sie hinzufügt zur Berechnung der Breaks
        period_starts.append(cur_period)
    diffs = [t - s for s, t in zip(period_starts, period_starts[1:])]
    in_time = check_in_time(periodicity)
    return len([x for x in diffs if x > in_time])
