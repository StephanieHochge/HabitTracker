import pandas as pd
import db
from datetime import date, timedelta
import dateutil.relativedelta


# Create a pandas dataframe from database tables
def create_data_frame(data_base, table):
    """
    creates a pandas dataframe from database tables
    :param data_base: the database which contains the desired table
    :param table: the table to be created - either "Habit", "HabitAppUser" or "Completion"
    :return: dataframe from the table
    """
    habit_columns = ["PKHabitID", "FKUserID", "Name", "Periodicity", "CreationTime"]
    # TODO: Überprüfen: Gibt es eine bessere Möglichkeit, die Table Header zu übergeben?
    user_columns = ["PKUserID", "UserName"]
    completion_columns = ["PKCompletionID", "FKHabitID", "CompletionDate"]
    column_names = {"Habit": habit_columns, "HabitAppUser": user_columns, "Completion": completion_columns}
    sql_query = pd.read_sql_query(f'''SELECT * FROM {table}''', data_base)
    return pd.DataFrame(sql_query, columns=column_names[table])


# return the user_id of a user
def return_user_id(data_base, user_name):
    """
    returns the user_id of a user
    :param data_base: the database which contains user data
    :param user_name: the user's user name
    :return: the user's user_id
    """
    user_df = create_data_frame(data_base, "HabitAppUser")
    user_id = user_df.loc[user_df["UserName"] == user_name]
    return user_id.iloc[0, 0]


# filter for data records containing the habits of a specific user
def return_user_habits(data_base, user_name):
    """

    :param data_base: the database which contains the habit data
    :param user_name: the user's user name
    :return: a pandas data frame containing the habits of the user and other data
    """
    user_id = return_user_id(data_base, user_name)
    habit_df = create_data_frame(data_base, "Habit")
    return habit_df.loc[habit_df["FKUserID"] == user_id]


# return the habit_id of a user's habit
def return_habit_id(data_base, habit_name, user_name):
    """

    :param data_base: the data_base which contains the data
    :param habit_name: the name of the habit, for which the habit_id is to be found
    :param user_name: the name of the user to which the habit belongs
    :return: the habit id (int)
    """
    user_habits = return_user_habits(data_base, user_name)
    habit = user_habits.loc[user_habits["Name"] == habit_name]
    return habit.iloc[0, 0]


# return completions of a specific habit
def return_habit_completions(data_base, habit_name, user_name):
    habit_id = return_habit_id(data_base, habit_name, user_name)
    completion_df = create_data_frame(data_base, "Completion")
    return completion_df.loc[completion_df["FKHabitID"] == habit_id]


# Return a list of all currently tracked habits of a user
def return_habits(data_base, user_name):
    """

    :param data_base: the database which contains the habit data
    :param user_name: the user's user name
    :return: a pandas series containing only the habits of the user
    """
    defined_habits = return_user_habits(data_base, user_name)
    return defined_habits["Name"]


# Filter for periodicity and return habits with said periodicity
def return_habits_of_type(data_base, user_name, periodicity):
    defined_habits = return_user_habits(data_base, user_name)
    habits_of_type = defined_habits.loc[defined_habits["Periodicity"] == periodicity]
    return habits_of_type["Name"]


# Return the longest habit streak for a given habit
def subtract_one_period(periodicity, check_date):
    """

    :param periodicity:
    :param check_date: of type string
    :return:
    """
    # TODO: Überprüfen, ob man das auch mit einem Dictionary machen kann
    check_date = date.fromisoformat(check_date)  # wandelt das Datum in ein Date-Format um
    previous_period = {}
    previous_period_start, previous_period_end = None, None
    if periodicity == "daily":
        period = timedelta(days=1)
        previous_period_start = check_date - period
        previous_period_end = check_date
    elif periodicity == "weekly":
        day_in_week = check_date.weekday()
        period_start = timedelta(days=day_in_week, weeks=1)
        period_end = timedelta(days=7)
        previous_period_start = check_date - period_start
        previous_period_end = previous_period_start + period_end
    elif periodicity == "monthly":
        day_in_month = check_date.day
        period = timedelta(days=day_in_month-1)
        previous_period_end = check_date - period
        previous_period_start = previous_period_end - dateutil.relativedelta.relativedelta(months=1)
    else:  # periodicity == yearly
        previous_year = check_date.year - 1
        previous_period_start = date.fromisoformat(f"{previous_year}-01-01")
        previous_period_end = date.fromisoformat(f"{check_date.year}-01-01")
    previous_period["start"] = previous_period_start
    previous_period["end"] = previous_period_end
    return previous_period


def check_previous_period(data_base, habit_name, user_name, previous_period):
    """
    checks whether habit has been completed in the previous period
    :param data_base:
    :param habit_name:
    :param user_name:
    :param previous_period: dictionary with start and end
    :return:
    """
    completions = return_habit_completions(data_base, habit_name, user_name)
    # filter for completions between previos_period_start and previous_period_end:
    completion_dates_str = completions["CompletionDate"]
    completion_dates = []
    for dates in completion_dates_str:  # create a list of all completion dates
        completion_dates.append(date.fromisoformat(dates))

    in_period = []
    for dates in completion_dates:
        if (dates >= previous_period["start"]) and (dates < previous_period["end"]):
            in_period.append("True")
            break
        else:
            in_period.append("False")
    print(in_period)
    return any(in_period)  # gibt "True" aus, wenn das für ein Datum stimmt und false, wenn es nicht stimmt
    # das funktioniert, aber ist das nicht vielleicht ein bisschen langsam? vielleicht kann man auch mit break stoppen?


def calculate_streak(check_date):
    """
    checks whether habit was completed in time considering its periodicity
    :return:
    """
    previous_period = subtract_one_period(check_date)
    previous_period_in_time = True
    streak = 0
    while previous_period_in_time:
        streak += 1
        previous_period_in_time = check_previous_period(the, the, the, previous_period, )
        previous_period = subtract_one_period(previous_period)

# Return the longest habit streak of all defined habits of a user


# Return the number of habit breaks


# Return the number of habit breaks during the last month
