from datetime import date, timedelta, datetime

import pandas as pd

import habit as hb


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
    completions_columns = ["CompletionsID", "FKHabitID", "CompletionDate", "CompletionTime"]
    column_names = {"Habit": habit_columns, "HabitAppUser": user_columns, "Completions": completions_columns}
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
    return user_id.iloc[0, 0]  # gibt einen Fehler aus, wenn es den User in der Datenbank nicht gibt - dies wird
    # allerdings nicht der Fall sein # TODO: trotzdem exception handling?


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
    return habit_df.loc[habit_df["FKUserID"] == user_id]  # wenn der User noch keine Habits hat, gibt dieser Befehl
    # ein empty Dataframe zurück


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
    completions_df = create_data_frame(habit.database, "Completions")
    habit_data = completions_df.loc[completions_df["FKHabitID"] == habit_id]
    return habit_data["CompletionDate"].to_list()


# return all completions of a user
def return_all_user_completions(user):
    """
    returns all completions for all habits of a user
    # TODO: test this function using pytest
    :param user:
    :return: a list of lists of all habit completions
    """
    habit_list = habit_creator(user)
    return list(map(return_habit_completions, habit_list))  # Problem: eine leere list of lists hat die Länge 1


def check_any_habit_data(user):
    """
    checks if any one habit of a user contains data
    :param user: the user in question
    :return: True/false (type: bool)
    """
    user_completions = return_all_user_completions(user)
    data_existing = [True for x in user_completions if len(x) > 0]
    return True if True in data_existing else False


# Return a list of all currently tracked habits of a user
def return_habits_only(user):
    """
    :param user: the user
    :return: a list containing only the habits of the user
    """
    defined_habits = return_user_habits(user)
    return defined_habits["Name"].to_list()


# return the periodicity of a habit.
def return_habit_periodicity(user, habit_name):  # can be used to load habit
    user_habits = return_user_habits(user)
    habit_data = user_habits.loc[user_habits["Name"] == habit_name]
    periodicity_series = habit_data["Periodicity"]
    return periodicity_series.to_list()[0]


# return a user's periodicities
def return_ordered_periodicites(user):
    defined_habits = return_user_habits(user)
    user_periodicities = (set(defined_habits["Periodicity"]))
    possible_periodicities = ["daily", "weekly", "monthly", "yearly"]
    return [x for x in possible_periodicities if x in user_periodicities]  # so that periodicities are in the correct
    # (ascending) order


# Filter for periodicity and return habits with said periodicity
def return_habits_of_type(user, periodicity):
    """

    :param user: the user (object)
    :param periodicity: the periodicity for which the user looks (str)
    :return: a pandas series with the names of the user's habits of the specified periodicity
    """
    defined_habits = return_user_habits(user)
    habits_of_type = defined_habits.loc[defined_habits["Periodicity"] == periodicity].reset_index()
    return habits_of_type[["Name", "CreationTime"]]


# change a list of dates as strings into a list of dates as datetime objects
def to_date_format(check_dates):
    return list(map(lambda x: date.fromisoformat(x), check_dates))


def weekly_start(check_date):
    """
    determines for any given date the date of the last Monday before that date, used for habits with weekly periodicity
    :param check_date: type: date
    :return: the date of the Monday before the passed in date
    """
    diff_to_start = timedelta(days=check_date.weekday())
    return check_date - diff_to_start


def monthly_start(check_date):
    """
    returns the first day of the month of the check_date
    :param check_date: type: date
    :return: the first day of the passed in month
    """
    diff_to_start = timedelta(days=check_date.day - 1)
    return check_date - diff_to_start


def yearly_start(check_date):
    """
    returns the first day of the year of the check_date
    :param check_date: type: date
    :return: the first day of the passed in year
    """
    return date.fromisoformat(f"{check_date.year}-01-01")


# calculate the period start for one completion only
def calculate_one_period_start(periodicity, check_date):
    """
    calculates the start of the period when a habit with the specified periodicity was checked off
    :param periodicity: the habit's periodicty (type: str)
    :param check_date: the date the habit was checked off (type: date)
    :return: the start of the period as a date when the habit was checked off (type: date)
    """
    period_start = calculate_period_starts(periodicity, [check_date])
    return period_start[0]


# calculate the period start for each completion in a list, return list of period starts
def calculate_period_starts(periodicity, check_dates):
    """
    calculates the period starts for each check-off date of a habit
    :param periodicity: the habit's periodicity
    :param check_dates: the dates on which the habits were checked off (type: list, dates: either date or str)
    :return: a list of period starts (which can contain duplicates)
    """
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
    """
    removes duplicates in the inserted list and sorts the elements
    :param period_starts: the period starts generated by "calculate period starts" (type: list of date objects)
    :return: the sorted list of period_starts without duplicates (type: list of date objects)
    """
    return sorted(list(set(period_starts)))


# checks what time difference between two completions is allowed
def check_in_time(periodicity):
    """
    checks what time differences between two habit completions is allowed by the habit's periodicity
    :param periodicity: the periodicity of the habit (type: str)
    :return: the allowed timedifference (type: timedelta object)
    """
    timeliness = {"daily": timedelta(days=1),
                  "weekly": timedelta(days=7),
                  "monthly": timedelta(days=31),  # wenn ein Habit in einem Monat nicht durchgeführt wurde, ist das
                  # timedelta mind. 58 days
                  "yearly": timedelta(days=366)
                  }
    return timeliness[periodicity]


# add future period to list to correctly calculate streaks and breaks
def add_future_period(tidy_period_starts, periodicity):
    """
    adds the start of the period that lies two periods ahead of the current period
    :param tidy_period_starts: the sorted period start list without duplicates (type: list of date objects)
    :param periodicity: the periodicity of the corresponding habit (type: str)
    :return: a list of dates including the calculated future period (type: list of date objects)
    """
    period_starts = tidy_period_starts  # notwendig, weil sonst die eigentliche Liste verändert wird
    duration = check_in_time(periodicity)  # ungefähre Dauer einer Periode
    future_period = calculate_one_period_start(periodicity, date.today() + 2 * duration)  # Berechnung einer
    # zukünftigen Periode mit mindestens einer Periode Abstand zu der aktuellen Periode
    if period_starts[-1] != future_period:  # wenn die aktuelle Periode nicht in der aufgeräumten Liste enthalten ist,
        # wird sie hinzufügt zur Berechnung der Breaks
        period_starts.append(future_period)
    return period_starts


# prepare for streak and break analysis
# funktioniert
def return_final_period_starts(habit):
    """
    returns a clean list of periods, in which the habit was performed at least once
    :param habit: the habit which is to be analyzed (type: instance of type HabitDB)
    :return: a clean list of periods, in which the habit was performed at least once (type: list of date objects)
    """
    check_dates = return_habit_completions(habit)
    period_starts = calculate_period_starts(habit.periodicity, check_dates)
    tidy_periods = tidy_starts(period_starts)
    return add_future_period(tidy_periods, habit.periodicity)


# calculate the difference of two consecutive elements in a list
def diffs_list_elements(period_starts):
    """
    calculates the differences of two consecutive elements in a list
    :param period_starts: list of dates that correspond to the periods in which the habit was checked off, cleaned
    (duplicates removed and sorted), the future period was already added (type: list of date objects)
    :return: a list of differences between two consecutive dates (type: list of timedelta objects)
    """
    return [t - s for s, t in zip(period_starts, period_starts[1:])]


# funktioniert auch
def calculate_break_indices(tidy_periods, periodicity):
    """
    calculate the indices of the periods, after which a habit was broken
    :param tidy_periods: a list of the periods in which the habit was checked off at least once
    (type: list of date objects)
    :param periodicity: the habit's periodicity (type: str)
    :return: a list of the indices (type: list of integers)
    """
    diffs = diffs_list_elements(tidy_periods)
    in_time = check_in_time(periodicity)
    return [index for index, value in enumerate(diffs) if value > in_time]


# generate list of streak lengths of one habit
# funktioniert für die vier getesteten Habits
def calculate_streak_lengths(habit):
    """
    calculates for each habits the length of each streak
    :param habit: the habit for which the streak lengths are to be calculated (type: instance of the HabitDB class)
    :return: a list of the habit's streak lengths (type: list of integers)
    """
    # TODO: wird diese Funktion auch so verwendet? Wenn ja, dann get this to work for habits which have not been
    #  checked off yet
    period_starts_curr = return_final_period_starts(habit)
    break_indices = calculate_break_indices(period_starts_curr, habit.periodicity)  # es muss immer break indices
    # geben, weil ja die zukünftige Periode hinzugefügt wird
    streak_lengths = [-1]  # weil der erste Streak sonst in der folgenden Berechnung nicht berücksichtigt wird
    streak_lengths[1:] = break_indices  # anhängen der restlichen Break Indizes
    return diffs_list_elements(streak_lengths)


# calculate the longest streak of one habit
def calculate_longest_streak(habit):
    """
    calculates the longest streak of one habit
    :param habit: the habit for which the longest streak is to be calculated (type: instance of HabitDB class)
    :return: the longest streak of the habit (type: int)
    """
    check_dates = return_habit_completions(habit)  # kann schon null sein, wenn es keine completions gibt
    if not check_dates:
        return 0
    else:
        streak_lengths = calculate_streak_lengths(habit)
        return max(streak_lengths)


# create a list of the user's habits
def habit_creator(user):
    """
    creates a list of the user's habits
    :param user: the user for which the habit list is to be created (type: instance of UserDB class)
    :return: a list of habit objects (type: list of instances of the HabitDB class)
    """
    # TODO: Was passiert, wenn der User noch keine Habits angelegt hat?
    habit_list = return_habits_only(user)
    periodicities = return_user_habits(user)["Periodicity"].to_list()
    combined = list(zip(habit_list, periodicities))
    return list(map(lambda x: hb.HabitDB(x[0], x[1], user, user.database), combined))


def calculate_longest_streak_per_habit(habit_list):
    """
    calculates the longest streak per habit
    :param habit_list: a list of habits (type: list of instances of the HabitDB class)
    :return: a dictionary with the habit names as keys and their longest streaks as values
    """
    habit_names = [habit.name for habit in habit_list]  # verwende ich an einer anderen Stelle nochmal
    longest_streaks = map(calculate_longest_streak, habit_list)
    return dict(zip(habit_names, longest_streaks))


# calculate the longest streak of all habits
def calculate_longest_streak_of_all(habits_with_data):
    """
    calculates the longest streak of all tracked habits
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
    # TODO: Test and add documentation
    cur_period = calculate_one_period_start(periodicity, date.today())
    prev_period = calculate_one_period_start(periodicity, cur_period - timedelta(days=1))
    return True if prev_period in tidy_period_starts else False


def calculate_curr_streak(habit):
    final_periods = return_final_period_starts(habit)
    if not check_previous_period(final_periods, habit.periodicity):
        return 0 if not check_current_period(final_periods, habit.periodicity) else 1
    else:
        streak_lengths = calculate_streak_lengths(habit)
        return streak_lengths[-1]


def check_current_period(tidy_period_starts, periodicity):
    """
    checks whether a habit was performed in the current period
    :param tidy_period_starts: a list of the periods in which the habit was checked off at least once
    (type: list of date objects)
    :param periodicity: the habit's periodicity (type: str)
    :return: True if the current period is contained in the list of periods, False if not
    """
    cur_period = calculate_one_period_start(periodicity, date.today())
    return True if cur_period in tidy_period_starts else False


# calculate last month
def return_last_month():
    """
    calculates the last month (i.e., if today is the 15 of Februar, the last month would be January)
    :return: the number of the last month (type: int)
    """
    last_month = (date.today() - timedelta(days=date.today().day))
    return last_month.month, last_month.year


# calculate the number of breaks within a list of dates
# funktioniert
def calculate_breaks(habit):
    """
    calculates the number of breaks a habit has experienced
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
    return len(completed_periods_4_weeks)/no_possible_periods


def calculate_completion_rate_per_habit(habits_with_data):
    frequent_habits = [habit for habit in habits_with_data if habit.periodicity in ("daily", "weekly")]
    habit_names = [habit.name for habit in frequent_habits]
    completion_rates = list(map(calculate_completion_rate, frequent_habits))
    return dict(zip(habit_names, completion_rates))


def calculate_worst_completion_rate_of_all(habits_with_data):
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
    check_dates = list(map(return_habit_completions, habit_list))
    habit_indices = [index for index, value in enumerate(check_dates) if len(value) > 0]
    return [habit for index, habit in enumerate(habit_list) if index in habit_indices]


def analysis_index():
    return ["periodicity: ", "last completion: ", "longest streak: ", "current streak: ",
             "breaks total: ", "completion rate (last 4 weeks): "]


def detailed_analysis_of_all_habits(habit_list):
    habits_with_data = find_habits_with_data(habit_list)
    habit_names = [habit.name for habit in habits_with_data]
    analysis_data = [habit.analyze_habit() for habit in habits_with_data]
    analysis_dict = dict(zip(habit_names, analysis_data))
    pd.set_option("display.max_columns", None)
    return pd.DataFrame(analysis_dict, index=analysis_index())


def analysis_one_habit(data, habit_name):
    return pd.DataFrame(data, index=analysis_index(), columns=[habit_name])


def list_to_df(analysis, data):
    return pd.DataFrame({'Analysis': analysis, 'data': data})



# TODO: Überprüfen, dass ich überall "pass" gelöscht hab
