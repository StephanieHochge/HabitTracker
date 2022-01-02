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


### Return the longest habit streak for a given habit
# determines the first period of habit completion and the last one
def determine_start_end_periods(data_base, habit_name, user_name, periodicity):
    completions = return_habit_completions(data_base, habit_name, user_name)
    completions = completions.sort_values("CompletionDate")
    first_date = date.fromisoformat(completions.iloc[0, 2])
    last_date = date.fromisoformat(completions.iloc[-1, 2])
    if periodicity == "daily":
        first_period_start = first_date
        last_period_start = last_date
    elif periodicity == "weekly":
        diff_to_start = timedelta(days=first_date.weekday())  # difference of the first date to the start of the first period
        diff_to_end = timedelta(days=last_date.weekday())
        first_period_start = first_date - diff_to_start
        last_period_start = last_date - diff_to_end
    elif periodicity == "monthly":
        diff_to_start = timedelta(days=first_date.day-1)
        diff_to_end = timedelta(days=last_date.day-1)
        first_period_start = first_date - diff_to_start
        last_period_start = last_date - diff_to_end
    else:  # periodicity == yearly
        first_period_start = date.fromisoformat(f"{first_date.year}-01-01")
        last_period_start = date.fromisoformat(f"{last_date.year}-01-01")
    if first_period_start == last_period_start:
        return {"period_start": first_period_start, "last_period_start": None}
    else:
        return {"first_period_start": first_period_start, "last_period_start": last_period_start}


# check whether the habit has been completed in the period
def habit_completed_in_period():
    pass


# adds a new column to name the streaks
def define_streaks():
    pass


# calculates for each streak the count
def calculate_streak():
    pass

# Return the longest habit streak of all defined habits of a user


# Return the number of habit breaks


# Return the number of habit breaks during the last month
