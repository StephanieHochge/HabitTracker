import pandas as pd
import db
from datetime import date, timedelta
import dateutil.relativedelta


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


# checks if user name is already existing
def check_for_user(data_base, user_name):
    """
    checks if the entered user name is already existing
    :param data_base: the database containing the data
    :param user_name: the name of the user to be checked for
    :return: True if the user name already exists and false if not
    """
    user_df = create_data_frame(data_base, "HabitAppUser")
    users = list(user_df["UserName"])
    return True if user_name in users else False


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
    """

    :param data_base: the data_base which contains the data
    :param habit_name: the habit for which data is to be displayed
    :param user_name: the habit's user name for which data is to be displayed
    :return: a data frame containing all completions of the user's habit
    """
    habit_id = return_habit_id(data_base, habit_name, user_name)
    period_df = create_data_frame(data_base, "Period")
    return period_df.loc[period_df["FKHabitID"] == habit_id]


# Return a list of all currently tracked habits of a user
def return_habits(data_base, user_name):
    """

    :param data_base: the database which contains the habit data
    :param user_name: the user's user name
    :return: a pandas series containing only the habits of the user
    """
    defined_habits = return_user_habits(data_base, user_name)
    return defined_habits["Name"].to_list()


# returns the periodicity of a habit.
def return_periodicity(data_base, user_name, habit_name):
    defined_habits = return_user_habits(data_base, user_name)
    habit = defined_habits.loc[defined_habits["Name"] == habit_name]
    periodicity_series = habit["Periodicity"]
    periodicity = periodicity_series.to_list()[0]
    return periodicity


# Filter for periodicity and return habits with said periodicity
def return_habits_of_type(data_base, user_name, periodicity):
    """

    :param data_base: the database which contains the habit data
    :param user_name: the name of the user (str)
    :param periodicity: the periodicity for which the user looks (str)
    :return: a pandas series with the names of the user's habits of the specified periodicity
    """
    defined_habits = return_user_habits(data_base, user_name)
    habits_of_type = defined_habits.loc[defined_habits["Periodicity"] == periodicity]
    return habits_of_type["Name"]


### Return the longest habit streak for a given habit
# determine the start of the period
def determine_period_start(periodicity, check_date):
    """
    determines the start of the current period, in which the habit was completed
    :param periodicity: the periodicitiy of the habit (str)
    :param check_date: the date where the habit was checked off (str), format: "YYYY-MM-DD"
    :return: the start of the current period (str), format: "YYYY-MM-DD"
    """
    check_date = date.fromisoformat(check_date)
    if periodicity == "daily":
        period_start = check_date
    elif periodicity == "weekly":
        diff_to_start = timedelta(days=check_date.weekday())
        period_start = check_date - diff_to_start
    elif periodicity == "monthly":
        diff_to_start = timedelta(days=check_date.day - 1)
        period_start = check_date - diff_to_start
    else:  # periodicity == yearly
        period_start = date.fromisoformat(f"{check_date.year}-01-01")
    period_start = str(period_start)
    return period_start


# determine the start of the next period
def determine_next_period_start(periodicity, check_date):
    """
    determines the start of the period that comes after the period in which the habit was checked off
    :param periodicity: the periodicitiy of the habit (str)
    :param check_date: the date where the habit was checked off (str), format: "YYYY-MM-DD"
    :return: the start of the next period (str), format: "YYYY-MM-DD"
    """
    check_date = date.fromisoformat(check_date)
    if periodicity == "daily":
        next_period_start = check_date + timedelta(days=1)
    elif periodicity == "weekly":
        diff_to_start = timedelta(days=7 - check_date.weekday())
        next_period_start = check_date + diff_to_start
    elif periodicity == "monthly":
        diff_to_start = timedelta(days=check_date.day - 1)
        period_start = check_date - diff_to_start
        next_period_start = period_start + dateutil.relativedelta.relativedelta(months=1)
    else:  # periodicity == yearly
        next_period_start = date.fromisoformat(f"{check_date.year + 1}-01-01")
    next_period_start = str(next_period_start)
    return next_period_start


# determine the start of the previous period
def determine_previous_period_start(periodicity, period_start):
    """
    determines the start of the period that came before the period in which the habit was checked off
    :param periodicity: the periodicitiy of the habit (str)
    :param period_start: the start of the period, in which the habit was checked off (str), format: "YYYY-MM-DD"
    :return: the start of the previous period (str), format: "YYYY-MM-DD"
    """
    period_start = date.fromisoformat(period_start)
    previous_period_end = str(period_start - timedelta(days=1))
    previous_period_start = determine_period_start(periodicity, previous_period_end)
    return str(previous_period_start)


# calculates for each streak the count
def calculate_streak_counts(data_base, habit_name, user_name):
    """

    :param data_base: the database containing the data
    :param habit_name: the habit for which the streak counts are to be returned (str)
    :param user_name: the habit's user (str)
    :return: a Pandas series containing the streak names as indexes and the counts
    """
    habit_completions = return_habit_completions(data_base, habit_name, user_name)
    habit_completions = habit_completions.drop_duplicates(subset="PeriodStart")  # Pro Periode wird nur ein Habit
    # gezählt (ein Habit kann mehrmals während einer Periode durchgeführt werden, dadurch erhöht sich aber nicht der
    # Streak)
    streaks = habit_completions.groupby(["StreakName"]).count()["PKPeriodID"]
    return streaks


# return the longest habit streak of the given habit
def return_longest_streak_for_habit(data_base, habit_name, user_name):
    """

    :param data_base: the database containing the data
    :param habit_name: the habit for which the longest streak is to be returned (str)
    :param user_name: the habit's user (str)
    :return: the longest streak of the given habit (int)
    """
    streaks = calculate_streak_counts(data_base, habit_name, user_name)
    return streaks.agg("max")  # returns the maximum value of the series

# Return the longest habit streak of all defined habits of a user


# Return the number of habit breaks


# Return the number of habit breaks during the last month
