import sqlite3
from sqlite3 import Error
from datetime import datetime


def get_db(name):
    """create a sqlite database connection with the specified table schema and the passed name

    :param name: the name of the database connection (type: str)
    :return: a database connection to the sqlite database with the specified name (type: sqlite3 connection)
    """
    try:
        database = sqlite3.connect(name)
    except Error as e:  # TODO: Entscheiden: drin lassen oder rausnehmen?
        print(e)
    else:
        database.execute("PRAGMA foreign_keys = 1")  # otherwise, on delete cascade does not work
        create_tables(database)
        return database


def create_tables(database):
    """create the data schema for the database containing three tables: the HabitAppUser, the Habit and the
    Completions table.

    :param database: the database connection in which the tables are to be created
    """
    cursor = database.cursor()

    # create HabitAppUser table
    user_table = """CREATE TABLE IF NOT EXISTS HabitAppUser
    (PKUserID INTEGER PRIMARY KEY, UserName TEXT)"""

    cursor.execute(user_table)

    # create Habit table
    habit_table = """CREATE TABLE IF NOT EXISTS Habit
    (PKHabitID INTEGER PRIMARY KEY, FKUserID INTEGER, Name TEXT, Periodicity TEXT, CreationTime TIMESTAMP,
    FOREIGN KEY(FKUserID) REFERENCES HabitAppUser(PKUserID) ON DELETE CASCADE ON UPDATE CASCADE)"""

    cursor.execute(habit_table)

    # create Completions table
    completions_table = """CREATE TABLE IF NOT EXISTS Completions
    (PKCompletionsID INTEGER PRIMARY KEY, FKHabitID INTEGER, CompletionDate DATE, CompletionTime TIME, 
    FOREIGN KEY(FKHabitID) REFERENCES Habit(PKHabitID) ON DELETE CASCADE ON UPDATE CASCADE)"""

    cursor.execute(completions_table)

    database.commit()


# insert data into tables
def add_user(user):
    """add user data into the table

    :param user:
    :return:
    """
    db = user.database
    cursor = db.cursor()
    cursor.execute("INSERT INTO HabitAppUser(UserName) VALUES (?)", [user.username])
    db.commit()


def find_user_id(user):
    db = user.database
    cursor = db.cursor()
    cursor.execute("SELECT PKUserID FROM HabitAppUser WHERE UserName = ?", [user.username])
    user_id = cursor.fetchone()
    return user_id[0]


def add_habit(habit, creation_time=None):
    db = habit.database
    cursor = db.cursor()
    user_id = find_user_id(habit.user)
    if not creation_time:
        creation_time = str(datetime.now())
    cursor.execute("INSERT INTO Habit(FKUserID, Name, Periodicity, CreationTime) VALUES (?, ?, ?, ?)",
                   (user_id, habit.name, habit.periodicity, creation_time))
    db.commit()


def find_habit_id(habit):
    """
    returns the habit id of a user's habit
    :param habit: the habit for which the id is to be returned
    :return: the habit's id (int)
    """
    cursor = habit.database.cursor()
    user_id = find_user_id(habit.user)
    cursor.execute("SELECT PKHabitID FROM Habit WHERE Name = ? AND FKUserID = ?",
                   (habit.name, user_id))  # sucht nach der HabitID des gesuchten Habits von dem User
    habit_id = cursor.fetchone()  # enthält list of tuples, weshalb das erste Element referenziert werden muss
    return habit_id[0]


def add_completion(habit, check_datetime=None):
    """
    adds a new completion to the completion table with the correct streak affiliation
    :param habit: the habit for which a new period is to be added
    :param check_datetime: the datetime on which the habit was checked off (type: str)
    :return: --
    """
    db = habit.database
    cursor = db.cursor()
    if not check_datetime:
        check_datetime = str(datetime.now())
    check_date, check_time = check_datetime.split(" ")
    habit_id = find_habit_id(habit)
    cursor.execute("INSERT INTO Completions(FKHabitID, CompletionDate, CompletionTime) VALUES (?, ?, ?)",
                   (habit_id, check_date, check_time))
    db.commit()


# delete habit and the corresponding habit data
def delete_habit(habit):
    habit_id = find_habit_id(habit)
    cursor = habit.database.cursor()
    cursor.execute("DELETE FROM Habit WHERE PKHabitID == ?", [habit_id])
    habit.database.commit()


# modify the habit's name, periodicity oder both
def modify_habit(habit, name, periodicity):
    habit_id = find_habit_id(habit)
    cursor = habit.database.cursor()
    if name:
        cursor.execute("UPDATE Habit SET Name = ? WHERE PKHabitID == ?", (name, habit_id))
    if periodicity:
        cursor.execute("UPDATE Habit SET Periodicity = ? WHERE PKHabitID == ?", (periodicity, habit_id))
    habit.database.commit()


# check if data was already entered to the user table
def user_data_existing(database):
    cursor = database.cursor()
    cursor.execute("SELECT * From HabitAppUser")
    return cursor.fetchall()


# TODO: Muss die Datenbank auch noch geschlossen werden? Dafür kann auch ein Context Manager eingesetzt werden:
# https://www.youtube.com/watch?v=ZsvftkbbrR0 (ab 12:43 Min)
