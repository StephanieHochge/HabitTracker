import sqlite3
from datetime import date, datetime
import analyze as an
import os


# TODO: Entscheidung: Ist es erlaubt, Max's Datenbank-Code zu verwenden?
def get_db(name="main.db"):
    database = sqlite3.connect(name)
    create_tables(database)
    return database


def create_tables(database):
    cursor = database.cursor()

    # create HabitAppUser table
    user_table = """CREATE TABLE IF NOT EXISTS HabitAppUser
    (PKUserID INTEGER PRIMARY KEY, UserName TEXT)"""

    cursor.execute(user_table)

    # create Habit table
    habit_table = """CREATE TABLE IF NOT EXISTS Habit
    (PKHabitID INTEGER PRIMARY KEY, FKUserID INTEGER, Name TEXT, Periodicity TEXT, CreationTime TEXT,
    FOREIGN KEY(FKUserID) REFERENCES HabitAppUser(PKUserID))"""

    cursor.execute(habit_table)

    # create Period table
    period_table = """CREATE TABLE IF NOT EXISTS Period
    (PKPeriodID INTEGER PRIMARY KEY, FKHabitID INTEGER, PeriodStart TEXT, CompletionDate TEXT, StreakName INTEGER, 
    FOREIGN KEY(FKHabitID) REFERENCES Habit(PKHabitID))"""

    cursor.execute(period_table)

    database.commit()


# add data into tables
def add_user(db, user_name):
    cursor = db.cursor()
    cursor.execute("INSERT INTO HabitAppUser(UserName) VALUES (?)", [user_name])
    db.commit()
    # TODO: Sicherstellen, dass UserName nicht bereits existiert (möglicherweise mit sqlite3.IntegrityError?)


def add_habit(db, user_name, name, periodicity, creation_time=None):
    cursor = db.cursor()
    cursor.execute("SELECT PKUserID FROM HabitAppUser WHERE UserName = ?", [user_name])
    user_id = cursor.fetchone()
    if not creation_time:
        creation_time = str(datetime.now())
    cursor.execute("INSERT INTO Habit(FKUserID, Name, Periodicity, CreationTime) VALUES (?, ?, ?, ?)",
                   (user_id[0], name, periodicity, creation_time))
    db.commit()
    # TODO: Sicherstellen, dass User nicht schon ein Habit mit demselben Namen hat


def return_habit_id(db, habit_name, user_name):
    """
    returns the habit id of a user's habit
    :param db: the database containing the data
    :param habit_name: the name of the habit for which the habit_id shall be returned (str)
    :param user_name: the name of the habit's user (str)
    :return: the habit's id (int)
    """
    cursor = db.cursor()
    cursor.execute("SELECT PKUserID FROM HabitAppUser WHERE UserName = ?", [user_name])
    user_id = cursor.fetchone()
    cursor.execute("SELECT PKHabitID FROM Habit WHERE Name = ? AND FKUserID = ?",
                   (habit_name, user_id[0]))  # sucht nach der HabitID des gesuchten Habits von dem User
    habit_id = cursor.fetchone()  # enthält list of tuples, weshalb das erste Element referenziert werden muss
    return habit_id[0]


def sql_streak_name(db, start_date, habit_id):
    """
    returns the name of the streak of a given habit in a specified period
    :param db: the database containing the data
    :param start_date: the start date of the period, for which the streak name shall be returned (str)
    :param habit_id: the id of the habit for which the streak name shall be returned (int)
    :return: a tuple containing the streak name if one exists
    """
    cursor = db.cursor()
    cursor.execute("SELECT StreakName FROM Period WHERE PeriodStart = ? AND FKHabitID = ?",
                   (start_date, habit_id))
    return cursor.fetchone()


def return_surrounding_streaks(db, habit_name, user_name, periodicity, check_date):
    """
    :param db: the database containing the data
    :param habit_name: the name of the habit for which the streak names are to be returned (str)
    :param user_name: the name of the habit's user (str)
    :param periodicity: the periodicity of the habit (str)
    :param check_date: the date when the habit was checked off (str), format: "YYYY-MM-DD"
    :return: a tuple containing the habit's id (int), the name of the current streak of the current period (int),
    the name of the streak of the previous period (int), and the name of the streak of the next period (int)
    """
    habit_id = return_habit_id(db, habit_name, user_name)
    period_start = an.determine_period_start(periodicity, check_date)
    previous_period_start = an.determine_previous_period_start(periodicity, period_start)
    next_period_start = an.determine_next_period_start(periodicity, check_date)
    previous_streak = sql_streak_name(db, previous_period_start, habit_id)
    current_streak = sql_streak_name(db, period_start, habit_id)
    next_streak = sql_streak_name(db, next_period_start, habit_id)
    return habit_id, previous_streak, current_streak, next_streak


def return_streak_name(db, habit_name, periodicity, user_name, check_date):
    """
    determines the streak to which the current completion belongs
    :param db: the database containing the data
    :param habit_name: the name of the habit for which a new completion was added and the streak affiliation now needs
    to be determined (str)
    :param periodicity: the habit's periodicity (str)
    :param user_name: the habit's user (str)
    :param check_date: the date where the habit was checked off (str), format: "YYYY-MM-DD"
    :return: the streak to which the current completion belongs (int)
    """
    habit_id, previous_streak, current_streak, next_streak = \
        return_surrounding_streaks(db, habit_name, user_name, periodicity, check_date)
    cursor = db.cursor()
    if current_streak is not None:  # check whether habit has already been completed in this period
        streak_name = current_streak[0]
    elif previous_streak is not None:  # check whether habit has been completed in the previous period
        streak_name = previous_streak[0]
    elif next_streak is not None:  # check whether habit has been completed in the next period
        streak_name = next_streak[0]
    else:  # if none of the above is true, a new streak is started with the current habit completion
        cursor.execute("SELECT MAX(StreakName) FROM Period WHERE FKHabitID = ?", [habit_id])
        last_streak = cursor.fetchone()
        if last_streak[0] is not None:
            streak_name = last_streak[0] + 1
        else:
            streak_name = 1
    return streak_name


def rename_streaks(db, habit_name, user_name, periodicity, check_date):
    """
    determines whether streaks following the current completion date need to be renamed. If they do, this function
    renames them
    :param db: the database containing the data
    :param habit_name: the name of the habit for which the streaks following the current check_date are to be checked
    (str)
    :param user_name: the habit's user (ste)
    :param periodicity: the habit's periodicity (str)
    :param check_date: the date on which the habit was checked off (str), format: "YYYY-MM-DD"
    :return: --
    """
    habit_id, previous_streak, current_streak, next_streak = \
        return_surrounding_streaks(db, habit_name, user_name, periodicity, check_date)
    cursor = db.cursor()
    next_period_start = an.determine_next_period_start(periodicity, check_date)
    if current_streak != next_streak and next_streak is not None:
        next_period_existing = True
        while next_period_existing:
            cursor.execute("UPDATE Period SET StreakName = ? WHERE FKHabitID = ? AND PeriodStart = ?",
                           (current_streak[0], habit_id, next_period_start))
            db.commit()
            next_period_start = an.determine_next_period_start(periodicity, next_period_start)
            next_streak = sql_streak_name(db, next_period_start, habit_id)
            if next_streak is None:
                next_period_existing = False


def add_period(db, habit_name, user_name, check_date=None):
    """
    adds a new period to the period table with the correct streak affiliation
    :param db: the database containing the data
    :param habit_name: the name of the habit for which a new period is to be added
    :param user_name: the habit's user
    :param check_date: the date on which the habit was checked off
    :return: --
    """
    cursor = db.cursor()
    if not check_date:
        check_date = str(date.today())
    habit_id = return_habit_id(db, habit_name, user_name)
    cursor.execute("SELECT Periodicity FROM Habit WHERE PKHabitID = ?", [habit_id])
    periodicity = cursor.fetchone()[0]
    period_start = an.determine_period_start(periodicity, check_date)
    streak_name = return_streak_name(db, habit_name, periodicity, user_name, check_date)
    cursor.execute("INSERT INTO Period(FKHabitID, PeriodStart, CompletionDate, StreakName) VALUES (?, ?, ?, ?)",
                   (habit_id, period_start, check_date, streak_name))
    rename_streaks(db, habit_name, user_name, periodicity, check_date)
    db.commit()

# cursor.execute("INSERT INTO HabitAppUser VALUES(1, 'StephanieHochge')")
# cursor.execute("INSERT INTO Habit VALUES(1, 1, 'Brush Teeth', 'daily', '123')")
# cursor.execute("INSERT INTO Completion VALUES(1, 1, ?)", (str(date.today())))


# TODO: @Chris: kann man sich die Tabelle mit den Daten irgendwie anders anzeigen lassen als durch ein Select-Statement?
# TODO: Muss die Datenbank auch noch geschlossen werden? Dafür kann auch ein Context Manager eingesetzt werden:
# https://www.youtube.com/watch?v=ZsvftkbbrR0 (ab 12:43 Min)
