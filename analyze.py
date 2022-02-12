from datetime import date, timedelta, datetime
import db

import pandas as pd

import habit as hb


def create_data_frame(database, table):
    """create a pandas dataframe from one of the database tables

    :param database: the database which contains the desired tables and data (type: sqlite3.connection)
    :param table: the table to be created - either "Habit", "HabitAppUser" or "Completions" (type: str)
    :return: a data frame containing the table's data (type: pandas.core.frame.DataFrame)
    """
    habit_columns = ["PKHabitID", "FKUserID", "Name", "Periodicity", "CreationTime"]
    user_columns = ["PKUserID", "UserName"]
    completions_columns = ["PKCompletionsID", "FKHabitID", "CompletionDate", "CompletionTime"]
    column_names = {"Habit": habit_columns, "HabitAppUser": user_columns, "Completions": completions_columns}
    sql_query = pd.read_sql_query(f'''SELECT * FROM {table}''', database)
    return pd.DataFrame(sql_query, columns=column_names[table])


def check_for_username(user):
    """check if the entered username is already in use in the database, in which user data is stored

    :param user: the user (type: user.UserDB)
    :return: True if the user name already exists and false if not (type: bool)
    """
    user_df = create_data_frame(user.database, "HabitAppUser")
    users = list(user_df["UserName"])
    return True if user.username in users else False


def show_habit_data(user):
    """filter the Habit table for habit data of the specified user

    :param user: the user for whom habit data is to be shown (type: user.UserDB)
    :return: a data frame containing only the habits and their data for one user (type: pandas.core.frame.DataFrame)
    """
    user_id = db.find_user_id(user)
    habit_df = create_data_frame(user.database, "Habit")
    return habit_df.loc[habit_df["FKUserID"] == user_id]


def return_completions(habit):
    """return a list of the completion dates for a specific habit

    :param habit: the habit for which the completion dates are to be returned (type: habit.HabitDB)
    :return: a list (type: list) containing all completion dates (type: str) of the habit
    """
    habit_id = db.find_habit_id(habit)
    completions_df = create_data_frame(habit.database, "Completions")
    habit_data = completions_df.loc[completions_df["FKHabitID"] == habit_id]
    return habit_data["CompletionDate"].to_list()


def return_ordered_periodicities(user):
    """return a user's periodicities in the correct order (daily < weekly < monthly < yearly)

    :param user: the user for whom periodicities are to be returned (type: user.UserDB)
    :return: a list (type: list) of the correctly ordered periodicities (type: str)
    """
    user_periodicities = (set([habit.periodicity for habit in user.defined_habits]))
    possible_periodicities = ["daily", "weekly", "monthly", "yearly"]  # to determine the order in the next step
    return [x for x in possible_periodicities if x in user_periodicities]


def return_habit_info(user, periodicity=None):
    """return the name, periodicity and creation time of either all of the user's habits (periodicity = None) or
    only the habits with a certain periodicity.

    :param user: the user (type: user.UserDB)
    :param periodicity: the periodicity for which information is to be returned ('str')
    :return: a data frame containing the name, periodicity and creation time of the desired habits
    (type: pandas.core.frame.DataFrame)
    """
    habit_info = show_habit_data(user)
    if periodicity:
        habit_info = habit_info.loc[habit_info["Periodicity"] == periodicity].reset_index()
    return habit_info[["Name", "Periodicity", "CreationTime"]]


def str_to_date(str_dates):
    """convert a list of dates as strings into a list of dates as datetime dates

    :param str_dates: list (type: list) of dates as strings (type: str)
    :return: a list (type: list) of datetime dates (type: datetime.date)
    """
    return list(map(lambda x: date.fromisoformat(x), str_dates))


def weekly_start(check_date):
    """for the given date, determine the date of the preceding Monday (to determine the period start for weekly
    habits). The period start is defined as the date where the period starts (is each day for daily habits and
    each Monday for weekly habits etc.).

    :param check_date: the completion date for which the period start is to be determined (type: datetime.date)
    :return: the date of the Monday before the passed in date (type: datetime.date)
    """
    diff_to_monday = timedelta(days=check_date.weekday())
    return check_date - diff_to_monday


def monthly_start(check_date):
    """determine the first day of the month of the passed in date

    :param check_date: the completion date for which the period start is to be determined (type: datetime.date)
    :return: the first day of the passed in month (type: datetime.date)
    """
    diff_to_first = timedelta(days=check_date.day - 1)
    return check_date - diff_to_first


def yearly_start(check_date):
    """determine the first day of the year of the passed in date

    :param check_date: the completion date for which the period start is to be determined (type: datetime.date)
    :return: the first day of the passed in year (type: datetime.date)
    """
    return date.fromisoformat(f"{check_date.year}-01-01")


def calculate_period_starts(periodicity, check_dates):
    """for each completion date of a habit, calculate the period start. The period start is defined as the date where
    the period starts (is each day for daily habits and each Monday for weekly habits etc.)

    :param periodicity: the habit's periodicity (type: str)
    :param check_dates: a list (type: list) of the habit's completion dates (dates: datetime.date or str)
    :return: a list (type: list) of period starts (type: datetime.date) - can contain duplicates
    """
    if isinstance(check_dates[0], str):  # are dates already in datetime.date format?
        check_dates = str_to_date(check_dates)
    period_start_funcs = {
        "daily": (lambda x: x),
        "weekly": weekly_start,
        "monthly": monthly_start,
        "yearly": yearly_start
    }
    period_start_func = period_start_funcs[periodicity]  # determine the correct function to calculate period starts
    return list(map(period_start_func, check_dates))  # calculate for each completion date the period start


def calculate_one_period_start(periodicity, check_date):
    """calculate the start of the period when a habit with the specified periodicity was completed

    :param periodicity: the habit's periodicty (type: str)
    :param check_date: the date the habit was checked off (type: datetime.date)
    :return: the start of the period (type: datetime.date)
    """
    period_start = calculate_period_starts(periodicity, [check_date])
    return period_start[0]


def tidy_starts(period_starts):
    """remove duplicates in the inserted list and sort the elements

    :param period_starts: a list (type: list) of period starts (type: datetime.date)
    :return: a sorted list (type: list) of period starts (type: datetime.date) without duplicates
    """
    return sorted(list(set(period_starts)))


def return_allowed_time(periodicity):
    """check what time difference is allowed between two habit completions according to the habit's periodicity
    so that the streak is not broken

    :param periodicity: the habit's periodicity (type: str)
    :return: the allowed time difference (type: datetime.timedelta)
    """
    timeliness = {"daily": timedelta(days=1),
                  "weekly": timedelta(days=7),
                  "monthly": timedelta(days=32),  # if a habit has not been completed in a month, the timedelta is at
                  # least 58 days
                  "yearly": timedelta(days=366)
                  }
    return timeliness[periodicity]


def add_future_period(tidy_period_starts, periodicity):
    """add a future period to correctly calculate streaks and breaks

    :param tidy_period_starts: the sorted list (type: list) of period starts (type: datetime.dates) without duplicates
    :param periodicity: the habit's periodicity (type: str)
    :return: a list (type: list) of period starts (type: datetime.date) including the calculated future period
    """
    period_starts = tidy_period_starts  # so as not to change the actual list
    duration = return_allowed_time(periodicity)  # approximate duration of a period
    future_period = calculate_one_period_start(periodicity, date.today() + 2 * duration)  # calculate a future period
    # with at least one period distance to the current period
    period_starts.append(future_period)
    return period_starts


# prepare for streak and break analysis
def return_final_period_starts(habit):
    """prepare for streak and break analysis by performing all functions necessary to return a clean list of periods,
    in which the habit was performed at least once, including the future period to correctly calculate break indices.

    :param habit: the habit which is to be analyzed (type: habit.HabitDB)
    :return: a clean list (type: list) of period starts (type: datetime.date), marking the start of periods,
    in which the habit was performed at least once
    """
    check_dates = return_completions(habit)
    period_starts = calculate_period_starts(habit.periodicity, check_dates)
    tidy_periods = tidy_starts(period_starts)
    return add_future_period(tidy_periods, habit.periodicity)


def calculate_element_diffs(final_periods):
    """calculate the differences between two consecutive elements in a list

    :param final_periods: clean list (type: list) of dates (type: datetime.date) that correspond to the start
     of the periods, in which the habit was checked off, including one future period
    :return: a list (type: list) of differences (type: datetime.timedelta) between two consecutive period starts
    """
    return [t - s for s, t in zip(final_periods, final_periods[1:])]


def calculate_break_indices(final_periods, periodicity):
    """return for the list of final periods the indices, of the periods, after which a habit streak was broken
    (i.e., the indices, after which at least one period is missing in the course of time)

    :param final_periods: clean list (type: list) of dates (type: datetime.date) that correspond to the start
     of the periods, in which the habit was checked off, including one future period
    :param periodicity: the habit's periodicity (type: str)
    :return: a list (type: list) of the indices (type: int) which indicate the break of a streak
    """
    diffs = calculate_element_diffs(final_periods)
    allowed_time = return_allowed_time(periodicity)
    return [index for index, value in enumerate(diffs) if value > allowed_time]


def calculate_streak_lengths(habit):
    """for a habit, calculate the length of each streak (i.e., the number of periods in a row, in which the habit was
    completed at least once)

    :param habit: the habit for which the streak lengths are to be calculated (type: habit.HabitDB)
    :return: a list (type: list) of the habit's streak lengths (type: int)
    """
    final_periods = return_final_period_starts(habit)
    break_indices = calculate_break_indices(final_periods, habit.periodicity)  # due to the added future period,
    # there is always at least one break index, even if no streak has been broken yet
    streak_lengths = [-1]  # because otherwise the following calculation does not consider the first streak
    streak_lengths[1:] = break_indices  # append the remaining break indices
    return calculate_element_diffs(streak_lengths)


def calculate_longest_streak(habit):
    """calculate the longest streak of a habit

    :param habit: the habit for which the longest streak is to be calculated (type: habit.HabitDB)
    :return: the habit's longest streak (type: int)
    """
    streak_lengths = calculate_streak_lengths(habit)
    return max(streak_lengths)


def habit_creator(user):
    """create a list of the user's habits

    :param user: the user for whom the habit list is to be created (type: user.UserDB)
    :return: a list (type: list) of habits (type: habit.HabitDB)
    """
    habit_data = show_habit_data(user)
    names_and_periodicity = habit_data[["Name", "Periodicity"]].values.tolist()
    return list(map(lambda x: hb.HabitDB(x[0], x[1], user, user.database), names_and_periodicity))


def calculate_longest_streak_per_habit(completed_habits):
    """calculate the longest streak for each habit in the passed in list of habits

    :param completed_habits: a list (type: list) of habits which have been completed at least once (type: habit.HabitDB)
    :return: a dictionary (type: dict) with the habit names (type: str) as keys and their longest streaks (type: int) 
    as values
    """
    if len(completed_habits) == 0:
        return None
    else:
        habit_names = [habit.name for habit in completed_habits]
        longest_streaks = map(calculate_longest_streak, completed_habits)
        return dict(zip(habit_names, longest_streaks))


def calculate_longest_streak_of_all(completed_habits):
    """calculate the longest streak of all tracked habits. The habit with the longest streak is defined as the habit
    completed the most periods in a row (i.e., a daily habit has a better chance of becoming the best habit than
    a yearly habit)

    :param completed_habits: a list (type: list) of habits (type: habit.HabitDB) that have been completed at least once
    :return: the value of the longest streak of all habits as well as the corresponding habit name (or habit names,
    since it is possible that several habits have the same longest streak)
    """
    longest_streaks = calculate_longest_streak_per_habit(completed_habits)
    if not longest_streaks:  # if none of the user's habits have been completed
        return None, None
    else:
        longest_streak_of_all = longest_streaks[max(longest_streaks, key=longest_streaks.get)]
        best_habits = [key for (key, value) in longest_streaks.items() if value == longest_streak_of_all]  # it is
        # possible that two habits have the same longest streak. In this way, both habits are returned.
        return longest_streak_of_all, best_habits


def completed_in_period(final_periods, periodicity, period):
    """check if the habit was completed in the passed in period.

    :param period: the period to check for, either "current" or "previous" (type: str)
    :param final_periods: clean list (type: list) of dates (type: datetime.date) that correspond to the start
     of the periods, in which the habit was checked off, including one future period
    :param periodicity: the habit's periodicity
    :return: true if the list of final periods contains the previous period, false otherwise (type: bool)
    """
    cur_period_start = calculate_one_period_start(periodicity, date.today())
    if period == "current":
        return True if cur_period_start in final_periods else False
    else:
        prev_period_start = calculate_one_period_start(periodicity, cur_period_start - timedelta(days=1))
        return True if prev_period_start in final_periods else False


def calculate_curr_streak(habit):
    """calculate the passed in habit's current streak.

    :param habit: the habit (type: habit.HabitDB), for which the current streak is to be calculated
    :return: the current streak (i.e., the current number of periods in a row, in which the user has
    completed the habit) (type: int)
    """
    final_periods = return_final_period_starts(habit)
    # if a habit was not completed in the previous period, the current streak is either 0 (not completed in
    # the current period) or 1 (completed in the current period)
    if not completed_in_period(final_periods, habit.periodicity, "previous"):
        return 0 if not completed_in_period(final_periods, habit.periodicity, "current") else 1
    else:
        streak_lengths = calculate_streak_lengths(habit)
        return streak_lengths[-1]


def calculate_break_no(habit):
    """calculate how often a habit's streaks were broken since the first completion

    :param habit: the habit which is to be analyzed (type: habit.HabitDB)
    :return: the number of breaks (type: int)
    """
    final_periods = return_final_period_starts(habit)
    break_indices = calculate_break_indices(final_periods, habit.periodicity)
    # if the habit was executed in the current or the previous period, there is one break less than elements in
    # break indices due to the consideration of the future period
    curr_period = completed_in_period(final_periods, habit.periodicity, "current")
    prev_period = completed_in_period(final_periods, habit.periodicity, "previous")
    if curr_period or prev_period:
        return len(break_indices) - 1
    else:
        return len(break_indices)


def calculate_completion_rate(habit):
    """calculate a habit's completion rate during the last 28 days (daily habits)/4 full weeks (weekly habits).
    Completions in the current period are not counted. The completion rate is defined as the number of periods
    in which the habit was completed divided by the number of periods in which the habit was not
    completed during the last four weeks. Is only calculated for daily or weekly habits.

    :param habit: the habit whose completion rate is to be calculated (type: habit.HabitDB)
    :return: the habit's completion rate during the last four weeks (type: float)
    """
    final_periods = return_final_period_starts(habit)
    no_possible_periods = 28 if habit.periodicity == "daily" else 4
    cur_period = calculate_one_period_start(habit.periodicity, date.today())
    period_4_weeks_ago = calculate_one_period_start(habit.periodicity, (cur_period - timedelta(weeks=4)))
    completed_periods_4_weeks = list(filter(lambda x: period_4_weeks_ago <= x < cur_period, final_periods))
    return len(completed_periods_4_weeks) / no_possible_periods


def calculate_completion_rate_per_habit(completed_habits):
    """for each daily or weekly habit that has been completed at least once, calculate the completion rate of
    the last four weeks

    :param completed_habits: a list (type: list) of completed habits (type: habit.HabitDB)
    :return: a dictionary (type: dict) with the name of each daily or weekly habit (type: str) as key and their
     completions rates (type: float) as values
    """
    frequent_habits = [habit for habit in completed_habits if habit.periodicity in ("daily", "weekly")]
    habit_names = [habit.name for habit in frequent_habits]
    completion_rates = list(map(calculate_completion_rate, frequent_habits))
    return dict(zip(habit_names, completion_rates))


def calculate_worst_completion_rate_of_all(completed_habits):
    """calculate from all daily and weekly habits that have been completed at least once the lowest completion rate.

    :param completed_habits: a list (type: list) of completed habits (type: habit.HabitDB)
    :return: a tuple (type: tuple) containing the lowest completion rate (type: float) and the name(s) of the
    habit(s) (type: str) that have the lowest completion rate(s)
    """
    completion_rates = calculate_completion_rate_per_habit(completed_habits)
    lowest_completion_rate = completion_rates[min(completion_rates, key=completion_rates.get)]
    worst_habits = [key for (key, value) in completion_rates.items() if value == lowest_completion_rate]  # it is
    # possible that two habits have the same completion rates. In this way, both are returned
    return lowest_completion_rate, worst_habits


def find_completed_habits(habit_list):
    """from a list of habits, identify the habits that have been completed at least once.

    :param habit_list: a list (type: list) of habits (type: habit.HabitDB)
    :return: a list (type: list) of habits (type: habit.HabitDB) that have been completed at least once
    """
    check_dates = list(map(return_completions, habit_list))
    habit_indices = [index for index, value in enumerate(check_dates) if len(value) > 0]
    return [habit for index, habit in enumerate(habit_list) if index in habit_indices]


def analysis_index():
    """return the index names for the analysis of habits"""
    return ["periodicity: ", "last completion: ", "longest streak: ", "current streak: ",
            "total breaks: ", "completion rate (last 4 weeks): "]


def analyze_all_habits(habit_list):
    """provide a detailed analysis of a user's habits that have been completed at least once.

    :param habit_list: a list (type: list) of all defined habits (type: habit.HabitDB) of a user
    :return: a dataframe (type: pandas.core.frame.DataFrame) containing a detailed analysis for each habit
    """
    completed_habits = find_completed_habits(habit_list)
    habit_names = [habit.name for habit in completed_habits]
    analysis_data = [habit.analyze_habit() for habit in completed_habits]
    analysis_dict = dict(zip(habit_names, analysis_data))
    pd.set_option("display.max_columns", None)  # to show all columns
    return pd.DataFrame(analysis_dict, index=analysis_index())


def present_habit_analysis(data, habit_name):
    """present the analysis of a habit as a data frame.

    :param data: a list (type: list) of the habit's statistics such as the longest streak, the current streak etc.
    :param habit_name: the name of the habit whose analysis is to be presented (type: str)
    :return: a dataframe presenting the habit's statistics (type: pandas.core.frame.DataFrame)
    """
    return pd.DataFrame(data, index=analysis_index(), columns=[habit_name])


def list_to_df(analysis, data):
    """turn two lists into a dataframe.

    :param analysis: a list (type: list) containg the type of analysis (type: str) that was carried out
    :param data: a list (type: list) containing the data that is to be displayed
    :return: a dataframe (type: pandas.core.frame.DataFrame) from the two lists
    """
    return pd.DataFrame({'Analysis': analysis, 'data': data})

# File wurde durchgegangen, jede Funktion ist dokumentiert und alle wichtigen Funktionen wurden getestet
