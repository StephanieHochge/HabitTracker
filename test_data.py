import os
from datetime import timedelta, datetime

import db
from habit import HabitDB
from user import UserDB


class DataForTesting:
    """This class creates test data for the application that can be used to the test the application's
    functionality using pytest. It provides four test users with a total of nine test habits. The test users differ
    in how many habits they have create (from zero to six) and whether they have already completed habits.
    Habits differ in their periodicity as well as in how often they were completed.

    Attributes:
        user_sh (user.UserDB): a test user with six habits, not all of which have already been completed
                                    (every available periodicity is used at least once by these habits).
        user_rb (user.UserDB): a test user with two habits which have the same streak length and completion rate.
        user_le (user.UserDB): a test user without any habits.
        user_hp (user.UserDB): a test user that has one habit that has not yet been completed.

        the following attributes are all habits ('habit.HabitDB') with varying periodicities,
        users and completion numbers:
        - teeth_rb
        - dance_rb
        - teeth_sh
        - dance_sh
        - windows_sh
        - bathroom_sh
        - dentist_sh
        - sleep_sh
        - conjure_hp
    """

    def create_users(self, database):
        """create the test users that are to be stored in the specified database

        :param database: the database connection where the test users are to be stored ('sqlite3.connection')
        """
        self.user_sh = UserDB("StephanieHochge", database)
        self.user_rb = UserDB("RajaBe", database)
        self.user_le = UserDB("LibertyEvans", database)
        self.user_hp = UserDB("HarryPotter", database)

    def store_users(self):
        """store the test users in the database"""
        db.add_user(self.user_sh)
        db.add_user(self.user_rb)
        db.add_user(self.user_le)
        db.add_user(self.user_hp)

    def create_habits(self):
        """create the test users' habits"""
        self.teeth_rb = HabitDB("Brush teeth", "daily", self.user_rb)
        self.dance_rb = HabitDB("Dance", "weekly", self.user_rb)
        self.teeth_sh = HabitDB("Brush teeth", "daily", self.user_sh)
        self.dance_sh = HabitDB("Dance", "weekly", self.user_sh)
        self.windows_sh = HabitDB("Clean windows", "monthly", self.user_sh)
        self.bathroom_sh = HabitDB("Clean bathroom", "weekly", self.user_sh)
        self.dentist_sh = HabitDB("Go to dentist", "yearly", self.user_sh)
        self.sleep_sh = HabitDB("Sleep", "daily", self.user_sh)
        self.conjure_hp = HabitDB("Conjuring", "daily", self.user_hp)

    def store_habits(self):
        """store the test users' habits in the database"""
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
        """store completion data for the test habits"""
        db.add_completion(self.teeth_rb)
        db.add_completion(self.teeth_rb, "2021-12-02 07:56:24.999098")

        db.add_completion(self.dance_rb, "2021-12-02 07:56:24.999098")
        db.add_completion(self.dance_rb, "2021-12-31 07:56:24.999098")

        db.add_completion(self.teeth_sh, "2021-12-01 07:56:24.999098")
        db.add_completion(self.teeth_sh, "2021-12-01 09:56:24.999098")
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
        db.add_completion(self.windows_sh, "2022-01-30 07:56:24.999098")
        db.add_completion(self.windows_sh)

        db.add_completion(self.dentist_sh, "2022-01-05 07:56:24.999098")
        db.add_completion(self.dentist_sh, "2021-12-05 07:56:24.999098")

        db.add_completion(self.teeth_sh, "2021-12-03 07:56:24.999098")

        db.add_completion(self.dance_sh, "2021-12-21 07:56:24.999098")
        db.add_completion(self.dance_sh)

    def create_test_data(self, database):
        """create all test data (i.e., users, habits, and habit completions) for the application

        :param database: the database connection in which the test data is to be stored ('sqlite3.connection')"""
        self.create_users(database)
        self.store_users()
        self.create_habits()
        self.store_habits()
        self.store_habit_completions()


class DataForTestingPytest(DataForTesting):
    """This class creates the test data provided by the DataForTesting class and stores is it in a
    test database. The data can then be used for testing the application's main functionalities using
    pytest.

    Attributes:
        database (sqlite3.connection): the test database which stores the test data.
        additional attributes: see the documentation of the DataForTesting class
    """
    def setup_method(self):
        """create the database connection, create the test data and save it in the database"""
        self.database = db.get_db("test.db")
        self.create_test_data(self.database)

    def teardown_method(self):
        """delete the test database after testing"""
        os.remove("test.db")


class DataForTestingCLI(DataForTesting):
    """This class creates the test data provided by the DataForTesting class and stores is it in the
    database specified. The data can then be used for testing the application's main functionalities using the CLI.

    Attributes:
        database ('sqlite3.connection'): the database which stores the test data.
        additional attributes: see the documentation of the DataForTesting class

    Parameters:
        database_name ('str'): the name of the database which stores the test data.
    """
    def __init__(self, database_name: str):
        self.database = db.get_db(database_name)
        self.create_test_data(self.database)

# Datentypen wurden angepasst und neben die Argumente geschrieben
