import sqlite3
from datetime import date, datetime


# TODO: Entscheidung: Ist es erlaubt, Max's Datenbank-Code zu verwenden?
def get_db(name="main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    cursor = db.cursor()

    # create HabitAppUser table
    user_table = """CREATE TABLE IF NOT EXISTS HabitAppUser
    (PKUserID INTEGER PRIMARY KEY, UserName TEXT)"""

    cursor.execute(user_table)

    # create Habit table
    habit_table = """CREATE TABLE IF NOT EXISTS Habit
    (PKHabitID INTEGER PRIMARY KEY, FKUserID INTEGER, Name TEXT, Periodicity TEXT, CreationTime TEXT,
    FOREIGN KEY(FKUserID) REFERENCES HabitAppUser(PKUserID))"""

    cursor.execute(habit_table)

    # create Completion table
    completion_table = """CREATE TABLE IF NOT EXISTS Completion
    (PKCompletionID INTEGER PRIMARY KEY, FKHabitID INTEGER, CompletionDate TEXT, 
    FOREIGN KEY(FKHabitID) REFERENCES Habit(PKHabitID))"""

    cursor.execute(completion_table)

    db.commit()


# add data into tables
def add_user(db, user_name):
    cursor = db.cursor()
    cursor.execute("INSERT INTO HabitAppUser(UserName) VALUES (?)", [user_name])  # eine ID müsste über AutoIncrement
    # automatisch hinzugefügt werden
    db.commit()

# cursor.execute("INSERT INTO HabitAppUser VALUES(1, 'StephanieHochge')")
# cursor.execute("INSERT INTO Habit VALUES(1, 1, 'Brush Teeth', 'daily', '123')")
# cursor.execute("INSERT INTO Completion VALUES(1, 1, ?)", (str(date.today())))


# TODO: @Chris: kann man sich die Tabelle mit den Daten irgendwie anders anzeigen lassen als durch ein Select-Statement?
