from datetime import date, timedelta, datetime
import db

import pandas as pd

import habit as hb

# TODO: vielleicht kann man die ganzen Funktionen, wo einfach nur Daten zurückgegeben werden in ein separates File
#  auslagern (außerhalb der Analyse, vielleicht in db?)
import user


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


# return all completions of a user
def return_all_completions(user):
    """return all completion dates for all habits of a user

    :param user: the user for whom all completion dates are to be returned
    :return: a list of lists of all habit completions
    """
    habit_list = habit_creator(user)
    return list(map(return_completions, habit_list))


def check_any_completions(user):
    """check if at least one habit of a user has been completed

    :param user: the user in question (type: user.UserDB)
    :return: True if at least one habit has been completed, false if not (type: bool)
    """
    user_completions = return_all_completions(user)
    data_existing = [True for x in user_completions if len(x) > 0]  # len(x) is > 0 if a habit has been completed
    return True if True in data_existing else False


def return_habit_names(user):
    """Return a list of the names of all currently tracked habits of a user

    :param user: the user in question (type: user.UserDB)
    :return: a list (type: list) containing only the habit names (type: str) of the user
    """
    defined_habits = show_habit_data(user)
    return defined_habits["Name"].to_list()


def return_periodicity(user, habit_name):
    """return the stored periodicity for a habit (e.g., to load the habit and its data).

    :param user: the habit's user (type: user.UserDB)
    :param habit_name: the name of the habit (type: str)
    :return: the habit's stored periodicity (type: str)
    """
    habit_data = show_habit_data(user)
    habit = habit_data.loc[habit_data["Name"] == habit_name]
    return habit["Periodicity"].to_list()[0]


def return_ordered_periodicites(user):
    """return a user's periodicities in the correct order (daily < weekly < monthly < yearly)

    :param user: the user for whom periodicities are to be returned (type: user.UserDB)
    :return: a list (type: list) of the correctly ordered periodicities (type: str)
    """
    defined_habits = show_habit_data(user)
    user_periodicities = (set(defined_habits["Periodicity"]))
    possible_periodicities = ["daily", "weekly", "monthly", "yearly"]  # to determine the order in the next step
    return [x for x in possible_periodicities if x in user_periodicities]


def return_habit_info(user, periodicity=None):
    """return the name, periodicity and creation time of either all of the user's habits (periodicity = None) or
    only the habits with a certain periodicity.

    :param user: the user (type: user.UserDB)
    :param periodicity: the periodicity for which infos are to be returned (str)
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


def allowed_time(periodicity):
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
    duration = allowed_time(periodicity)  # approximate duration of a period
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


def diffs_list_elements(period_starts):
    """calculate the differences of two consecutive elements in a list

    :param period_starts: list of dates that correspond to the periods in which the habit was checked off, cleaned
    (duplicates removed and sorted), the future period was already added (type: list of date objects)
    :return: a list of differences between two consecutive dates (type: list of timedelta objects)
    """
    return [t - s for s, t in zip(period_starts, period_starts[1:])]


def calculate_break_indices(tidy_periods, periodicity):
    """calculate the indices of the periods, after which a habit was broken

    :param tidy_periods: a list of the periods in which the habit was checked off at least once
    (type: list of date objects)
    :param periodicity: the habit's periodicity (type: str)
    :return: a list of the indices (type: list of integers)
    """
    diffs = diffs_list_elements(tidy_periods)
    in_time = allowed_time(periodicity)
    return [index for index, value in enumerate(diffs) if value > in_time]


# generate list of streak lengths of one habit
# funktioniert für die vier getesteten Habits
def calculate_streak_lengths(habit):
    """calculate for each habits the length of each streak

    :param habit: the habit for which the streak lengths are to be calculated (type: instance of the HabitDB class)
    :return: a list of the habit's streak lengths (type: list of integers)
    """
    period_starts_curr = return_final_period_starts(habit)
    break_indices = calculate_break_indices(period_starts_curr, habit.periodicity)  # es muss immer break indices
    # geben, weil ja die zukünftige Periode hinzugefügt wird
    streak_lengths = [-1]  # weil der erste Streak sonst in der folgenden Berechnung nicht berücksichtigt wird
    streak_lengths[1:] = break_indices  # anhängen der restlichen Break Indizes
    return diffs_list_elements(streak_lengths)


def calculate_longest_streak(habit):
    """calculate the longest streak of one habit

    :param habit: the habit for which the longest streak is to be calculated (type: instance of HabitDB class)
    :return: the longest streak of the habit (type: int)
    """
    check_dates = return_completions(habit)  # kann schon null sein, wenn es keine completions gibt
    if not check_dates:
        return 0
    else:
        streak_lengths = calculate_streak_lengths(habit)
        return max(streak_lengths)


def habit_creator(user):
    """create a list of the user's habits

    :param user: the user for whom the habit list is to be created (type: instance of UserDB class)
    :return: a list of habit objects (type: list of instances of the HabitDB class)
    """
    habit_list = return_habit_names(user)
    periodicities = show_habit_data(user)["Periodicity"].to_list()
    combined = list(zip(habit_list, periodicities))
    return list(map(lambda x: hb.HabitDB(x[0], x[1], user, user.database), combined))


def calculate_longest_streak_per_habit(habit_list):
    """calculate the longest streak per habit

    :param habit_list: a list of habits (type: list of instances of the HabitDB class)
    :return: a dictionary with the habit names as keys and their longest streaks as values
    """
    habit_names = [habit.name for habit in habit_list]  # verwende ich an einer anderen Stelle nochmal, ich hab auch
    # eine Funktion, die die Habit Names returned
    longest_streaks = map(calculate_longest_streak, habit_list)
    return dict(zip(habit_names, longest_streaks))


def calculate_longest_streak_of_all(habits_with_data):
    """calculate the longest streak of all tracked habits
    the habit with the longest streak is defined as the habit which was performed the most periods in a row (i.e., a
    daily habit has a better chance of becoming the best habit than a yearly habit)
    :param habits_with_data: a list of habits (type: list of instances of the HabitDB class)
    :return: the value of the longest streak of all habits as well as the corresponding habit name (or habit names,
    since it is possible that several habits have the same longest streak)
    """
    longest_streaks = calculate_longest_streak_per_habit(habits_with_data)
    if len(longest_streaks) == 0:  # wenn noch kein Habit completed wurde  # TODO: brauche ich das überhaupt noch?
        return None, None
    else:
        longest_streak_of_all = longest_streaks[max(longest_streaks, key=longest_streaks.get)]
        best_habits = [key for (key, value) in longest_streaks.items() if value == longest_streak_of_all]  # it is
        # possible that two habits have the same streak lengths, this way they would both be returned
        return longest_streak_of_all, best_habits


def check_previous_period(tidy_period_starts, periodicity):
    """

    :param tidy_period_starts:
    :param periodicity:
    :return:
    """
    # TODO: Test and add documentation
    cur_period = calculate_one_period_start(periodicity, date.today())
    prev_period = calculate_one_period_start(periodicity, cur_period - timedelta(days=1))
    return True if prev_period in tidy_period_starts else False


def calculate_curr_streak(habit):
    """

    :param habit:
    :return:
    """
    final_periods = return_final_period_starts(habit)
    if not check_previous_period(final_periods, habit.periodicity):
        return 0 if not check_current_period(final_periods, habit.periodicity) else 1
    else:
        streak_lengths = calculate_streak_lengths(habit)
        return streak_lengths[-1]


def check_current_period(tidy_period_starts, periodicity):
    """check whether a habit was performed in the current period

    :param tidy_period_starts: a list of the periods in which the habit was checked off at least once
    (type: list of date objects)
    :param periodicity: the habit's periodicity (type: str)
    :return: True if the current period is contained in the list of periods, False if not
    """
    cur_period = calculate_one_period_start(periodicity, date.today())
    return True if cur_period in tidy_period_starts else False


# calculate last month
def return_last_month():
    """calculate the last month (i.e., if today is the 15 of Februar, the last month would be January)

    :return: the number of the last month (type: int)
    """
    last_month = (date.today() - timedelta(days=date.today().day))
    return last_month.month, last_month.year


def calculate_breaks(habit):
    """calculate the number of breaks a habit has experienced since the first completion

    :param habit: the habit which is to be analyzed (type: instance of HabitDB class)
    :return: the number of breaks (type: int)
    """
    final_periods = return_final_period_starts(habit)
    break_indices = calculate_break_indices(final_periods, habit.periodicity)
    if check_current_period(final_periods, habit.periodicity):
        return len(break_indices) - 1  # wenn der Habit in der aktuellen Periode schon ausgeführt wurde, dann gibt es
        # eine Break weniger als break_indices ausrechnet (weil ja die zukünftige Periode mit berücksichtigt wird)
    else:
        return len(break_indices)


def calculate_completion_rate(habit):
    """

    :param habit:
    :return:
    """
    # only possible for daily and weekly habits
    # completion rate is the number of periods in which the habit was completed divided by the number of periods in
    # which the habit was not completed during the last four weeks
    # TODO: was passiert hier, wenn Habit noch nicht completed wurde?
    no_possible_periods = 28 if habit.periodicity == "daily" else 4
    final_periods = return_final_period_starts(habit)
    time_diff = timedelta(days=28) if habit.periodicity == "daily" else timedelta(weeks=4)
    period_4_weeks_ago = calculate_one_period_start(habit.periodicity, (date.today() - time_diff))
    cur_period = calculate_one_period_start(habit.periodicity, date.today())
    completed_periods_4_weeks = list(filter(lambda x: period_4_weeks_ago < x < cur_period, final_periods))
    return len(completed_periods_4_weeks) / no_possible_periods


def calculate_completion_rate_per_habit(habits_with_data):
    """

    :param habits_with_data:
    :return:
    """
    frequent_habits = [habit for habit in habits_with_data if habit.periodicity in ("daily", "weekly")]
    habit_names = [habit.name for habit in frequent_habits]
    completion_rates = list(map(calculate_completion_rate, frequent_habits))
    return dict(zip(habit_names, completion_rates))


def calculate_worst_completion_rate_of_all(habits_with_data):
    """

    :param habits_with_data:
    :return:
    """
    # man muss es schaffen, dass in dieser Habit-Liste nur Habits mit Daten ausgegeben werden
    completion_rates = calculate_completion_rate_per_habit(habits_with_data)
    lowest_completion_rate = completion_rates[min(completion_rates, key=completion_rates.get)]
    worst_habits = [key for (key, value) in completion_rates.items() if value == lowest_completion_rate]  # it is
    # possible that two habits have the same streak lengths, this way they would both be returned
    return lowest_completion_rate, worst_habits


def find_habits_with_data(habit_list):
    """
    returns only habits that contain data
    :param habit_list:
    :return:
    """
    check_dates = list(map(return_completions, habit_list))
    habit_indices = [index for index, value in enumerate(check_dates) if len(value) > 0]
    return [habit for index, habit in enumerate(habit_list) if index in habit_indices]


def analysis_index():
    """

    :return:
    """
    return ["periodicity: ", "last completion: ", "longest streak: ", "current streak: ",
            "total breaks: ", "completion rate (last 4 weeks): "]


def detailed_analysis_of_all_habits(habit_list):
    """

    :param habit_list:
    :return:
    """
    habits_with_data = find_habits_with_data(habit_list)
    habit_names = [habit.name for habit in habits_with_data]
    analysis_data = [habit.analyze_habit() for habit in habits_with_data]
    analysis_dict = dict(zip(habit_names, analysis_data))
    pd.set_option("display.max_columns", None)
    return pd.DataFrame(analysis_dict, index=analysis_index())


def analysis_one_habit(data, habit_name):
    """

    :param data:
    :param habit_name:
    :return:
    """
    return pd.DataFrame(data, index=analysis_index(), columns=[habit_name])


def list_to_df(analysis, data):
    """

    :param analysis:
    :param data:
    :return:
    """
    return pd.DataFrame({'Analysis': analysis, 'data': data})
