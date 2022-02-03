import os

import db
from habit import HabitDB
from user import UserDB
from datetime import date, timedelta, datetime


class TestData:

    def create_users(self, database):
        self.user_sh = UserDB("StephanieHochge", database)
        self.user_rb = UserDB("RajaBe", database)
        self.user_le = UserDB("LibertyEvans", database)
        self.user_hp = UserDB("HarryPotter", database)

    def store_users(self):
        db.add_user(self.user_sh)
        db.add_user(self.user_rb)
        db.add_user(self.user_le)
        db.add_user(self.user_hp)

    def create_habits(self):
        self.teeth_rb = HabitDB("Brush teeth", "daily", self.user_rb, self.user_rb.database)
        self.dance_rb = HabitDB("Dance", "weekly", self.user_rb, self.user_rb.database)
        self.teeth_sh = HabitDB("Brush teeth", "daily", self.user_sh, self.user_sh.database)
        self.dance_sh = HabitDB("Dance", "weekly", self.user_sh, self.user_sh.database)
        self.windows_sh = HabitDB("Clean windows", "monthly", self.user_sh, self.user_sh.database)
        self.bathroom_sh = HabitDB("Clean bathroom", "weekly", self.user_sh, self.user_sh.database)
        self.dentist_sh = HabitDB("Go to dentist", "yearly", self.user_sh, self.user_sh.database)
        self.sleep_sh = HabitDB("sleep", "daily", self.user_sh, self.user_sh.database)
        self.conjure_hp = HabitDB("Conjuring", "daily", self.user_hp, self.user_sh.database)

    def store_habits(self):
        db.add_habit(self.teeth_rb)
        db.add_habit(self.dance_rb)
        db.add_habit(self.teeth_sh, "2021-11-30 07:54:24.999098")
        db.add_habit(self.dance_sh, "2021-10-31 07:54:24.999098")
        db.add_habit(self.windows_sh, "2021-10-31 07:54:24.999098")
        db.add_habit(self.bathroom_sh, "2022-10-31 07:56:24.999098")
        db.add_habit(self.dentist_sh, "2022-10-31 07:56:24.999098")
        db.add_habit(self.sleep_sh)
        db.add_habit(self.conjure_hp)

    def store_habit_completions(self):
        db.add_completion(self.teeth_rb)
        db.add_completion(self.teeth_rb, "2022-12-02 07:56:24.999098")
        db.add_completion(self.dance_rb, "2021-12-02 07:56:24.999098")
        db.add_completion(self.dance_rb, "2021-12-31 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-01 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-01 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-02 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-02 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-02 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-04 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-05 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-07 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-08 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-09 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-10 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-11 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-12 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-13 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-14 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-15 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-16 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-17 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-18 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-19 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-20 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-21 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-22 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-23 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-24 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-25 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-26 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-27 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-29 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-30 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-31 07:56:24.999098")
        db.add_completion(self.teeth_sh, str(datetime.now() - timedelta(weeks=2, days=2)))
        db.add_completion(self.teeth_sh, str(datetime.now() - timedelta(weeks=1, days=1)))
        db.add_completion(self.teeth_sh, str(datetime.now() - timedelta(weeks=1)))
        db.add_completion(self.teeth_sh, str(datetime.now() - timedelta(weeks=1, days=3)))
        db.add_completion(self.teeth_sh, str(datetime.now() - timedelta(weeks=1, days=4)))
        db.add_completion(self.teeth_sh, str(datetime.now() - timedelta(weeks=1, days=5)))
        db.add_completion(self.dance_sh, "2021-11-06 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-11-07 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-11-11 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-11-13 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-11-14 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-11-21 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-11-25 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-11-27 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-11-28 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-12-02 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-12-04 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-12-05 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-12-16 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-12-18 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-12-19 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-12-30 07:56:24.999098")
        db.add_completion(self.dance_sh, str(datetime.now() - timedelta(weeks=1)))
        db.add_completion(self.dance_sh, str(datetime.now() - timedelta(weeks=2)))
        db.add_completion(self.bathroom_sh, "2021-11-06 07:56:24.999098")
        db.add_completion(self.bathroom_sh, "2021-11-13 07:56:24.999098")
        db.add_completion(self.bathroom_sh, "2021-11-20 07:56:24.999098")
        db.add_completion(self.bathroom_sh, "2021-12-04 07:56:24.999098")
        db.add_completion(self.bathroom_sh, "2021-12-11 07:56:24.999098")
        db.add_completion(self.bathroom_sh, "2021-12-18 07:56:24.999098")
        db.add_completion(self.bathroom_sh, "2022-01-01 07:56:24.999098")
        db.add_completion(self.windows_sh, "2021-06-23 07:56:24.999098")
        db.add_completion(self.windows_sh, "2021-07-06 07:56:24.999098")
        db.add_completion(self.windows_sh, "2021-09-15 07:56:24.999098")
        db.add_completion(self.windows_sh, "2021-10-02 07:56:24.999098")
        db.add_completion(self.windows_sh, "2021-11-17 07:56:24.999098")
        db.add_completion(self.windows_sh, "2021-12-30 07:56:24.999098")
        db.add_completion(self.windows_sh)
        db.add_completion(self.dentist_sh, "2022-01-05 07:56:24.999098")
        db.add_completion(self.dentist_sh, "2021-12-05 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-03 07:56:24.999098")
        db.add_completion(self.dance_sh, "2021-12-21 07:56:24.999098")
        db.add_completion(self.dance_sh)
        # Todo: am besten noch ein paar Daten mehr einfügen, die mit timedelta und now berechnet werden, damit die Tests
        #  immer stimmen und die App auch später noch gut getestet werden kann

    def create_test_data(self, database):
        self.create_users(database)
        self.store_users()
        self.create_habits()
        self.store_habits()
        self.store_habit_completions()


class TestDataPytest(TestData):
    def setup_method(self):
        self.database = db.get_db("test.db")
        self.create_test_data(self.database)

    def teardown_method(self):
        os.remove("test.db")  # löscht die Datenbank


class DataCli(TestData):
    def __init__(self, database):
        self.database = db.get_db(database)
        self.create_test_data(self.database)
