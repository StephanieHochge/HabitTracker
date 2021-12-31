import pandas as pd
import db


# Create a pandas dataframe from database tables
def create_data_frame(data_base, table):
    habit_columns = ["PKHabitID", "FKUserID", "Name", "Periodicity", "CreationTime"]
    # TODO: Überprüfen: Gibt es eine bessere Möglichkeit, die Table Header zu übergeben?
    user_columns = ["PKUserID", "UserName"]
    completion_columns = ["PKCompletionID", "FKHabitID", "CompletionDate"]
    column_names = {"Habit": habit_columns, "HabitAppUser": user_columns, "Completion": completion_columns}
    sql_query = pd.read_sql_query(f'''SELECT * FROM {table}''', data_base)
    return pd.DataFrame(sql_query, columns=column_names[table])


# Return a list of all currently tracked habits of a user
def return_user_habits(data_base, user_name):
    user_df = create_data_frame(data_base, "HabitAppUser")
    user_id = user_df["UserName"] == user_name
    habit_df = create_data_frame(data_base, "Habit")
    defined_habits = habit_df.loc[habit_df["FKUserID"] == user_id[0]]
    return defined_habits["Name"]

# Filter for periodicity and return habits with said periodicity


# Return the longest habit streak of all defined habits of a user


# Return the longest habit streak for a given habit


# Return the number of habit breaks


# Return the number of habit breaks during the last month
