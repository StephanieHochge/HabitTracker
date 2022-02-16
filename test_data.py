import os
from datetime import timedelta, datetime

import db
from habit import HabitDB
from user import UserDB


class DataForTesting:
    """This class creates test data for the application that can be used to the test the application's
    functionality at runtime or using pytest. It provides four test users with a total of nine test habits.
    The test users differ in how many habits they have created (from zero to six) and whether they have
    already completed habits. Habits differ in their periodicity as well as in how often they were completed.

    Attributes:
        harry_p (user.UserDB): a test user with six habits, not all of which have already been completed
                                    (every available periodicity is used at least once by these habits).
        hermione_g (user.UserDB): a test user with two habits which have the same streak length and completion rate.
        ron_w (user.UserDB): a test user without any habits.
        voldemort (user.UserDB): a test user with one habit that has not yet been completed.

        The following attributes are all habits ('habit.HabitDB') with varying periodicities,
        users and completion times:
        - study_hg
        - books_hg
        - hedwig_hp
        - ginny_hp
        - malfoy_hp
        - quidditch_hp
        - kill_voldemort_hp
        - conjure_hp
        - kill_harry_v
    """

    def create_users(self, database):
        """create the test users that are to be stored in the specified database

        :param database: the database connection where the test users are to be stored ('sqlite3.connection')
        """
        self.harry_p = UserDB("HarryP", database)
        self.hermione_g = UserDB("HermioneG", database)
        self.ron_w = UserDB("RonW", database)
        self.voldemort = UserDB("Voldemort", database)

    def store_users(self):
        """store the test users in the database"""
        db.add_user(self.harry_p)
        db.add_user(self.hermione_g)
        db.add_user(self.ron_w)
        db.add_user(self.voldemort)

    def create_habits(self):
        """create the test users' habits"""
        self.study_hg = HabitDB("Study", "daily", self.hermione_g)
        self.books_hg = HabitDB("Read books", "weekly", self.hermione_g)
        self.hedwig_hp = HabitDB("Feed Hedwig", "daily", self.harry_p)
        self.ginny_hp = HabitDB("Meet Ginny", "weekly", self.harry_p)
        self.malfoy_hp = HabitDB("Tease Malfoy", "monthly", self.harry_p)
        self.quidditch_hp = HabitDB("Train Quidditch", "weekly", self.harry_p)
        self.kill_voldemort_hp = HabitDB("Kill Voldemort", "yearly", self.harry_p)
        self.conjure_hp = HabitDB("Conjuring", "daily", self.harry_p)
        self.kill_harry_v = HabitDB("Kill Harry", "daily", self.voldemort)

    def store_habits(self):
        """store the test users' habits in the database"""
        db.add_habit(self.study_hg)
        db.add_habit(self.books_hg)
        db.add_habit(self.hedwig_hp, "2021-11-30 07:54:24.999098")
        db.add_habit(self.ginny_hp, "2021-10-31 07:54:24.999098")
        db.add_habit(self.malfoy_hp, "2021-10-31 07:54:24.999098")
        db.add_habit(self.quidditch_hp, "2022-10-31 07:56:24.999098")
        db.add_habit(self.kill_voldemort_hp, "2022-10-31 07:56:24.999098")
        db.add_habit(self.conjure_hp)
        db.add_habit(self.kill_harry_v)

    def store_habit_completions(self):
        """store completion data for the test habits"""
        db.add_completion(self.study_hg)
        db.add_completion(self.study_hg, "2021-12-02 07:56:24.999098")

        db.add_completion(self.books_hg, "2021-12-02 07:56:24.999098")
        db.add_completion(self.books_hg, "2021-12-31 07:56:24.999098")

        db.add_completion(self.hedwig_hp, "2021-12-01 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-01 09:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-02 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-02 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-02 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-04 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-05 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-07 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-08 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-09 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-10 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-11 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-12 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-13 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-14 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-15 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-16 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-17 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-18 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-19 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-20 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-21 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-22 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-23 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-24 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-25 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-26 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-27 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-29 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-30 07:56:24.999098")
        db.add_completion(self.hedwig_hp, "2021-12-31 07:56:24.999098")
        db.add_completion(self.hedwig_hp, str(datetime.now() - timedelta(weeks=2, days=2)))
        db.add_completion(self.hedwig_hp, str(datetime.now() - timedelta(weeks=1, days=1)))
        db.add_completion(self.hedwig_hp, str(datetime.now() - timedelta(weeks=1)))
        db.add_completion(self.hedwig_hp, str(datetime.now() - timedelta(weeks=1, days=3)))
        db.add_completion(self.hedwig_hp, str(datetime.now() - timedelta(weeks=1, days=4)))
        db.add_completion(self.hedwig_hp, str(datetime.now() - timedelta(weeks=1, days=5)))

        db.add_completion(self.ginny_hp, "2021-11-06 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-11-07 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-11-11 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-11-13 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-11-14 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-11-21 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-11-25 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-11-27 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-11-28 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-12-02 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-12-04 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-12-05 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-12-16 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-12-18 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-12-19 07:56:24.999098")
        db.add_completion(self.ginny_hp, "2021-12-30 07:56:24.999098")
        db.add_completion(self.ginny_hp, str(datetime.now() - timedelta(weeks=1)))
        db.add_completion(self.ginny_hp, str(datetime.now() - timedelta(weeks=2)))

        db.add_completion(self.quidditch_hp, "2021-11-06 07:56:24.999098")
        db.add_completion(self.quidditch_hp, "2021-11-13 07:56:24.999098")
        db.add_completion(self.quidditch_hp, "2021-11-20 07:56:24.999098")
        db.add_completion(self.quidditch_hp, "2021-12-04 07:56:24.999098")
        db.add_completion(self.quidditch_hp, "2021-12-11 07:56:24.999098")
        db.add_completion(self.quidditch_hp, "2021-12-18 07:56:24.999098")
        db.add_completion(self.quidditch_hp, "2022-01-01 07:56:24.999098")

        db.add_completion(self.malfoy_hp, "2021-06-23 07:56:24.999098")
        db.add_completion(self.malfoy_hp, "2021-07-06 07:56:24.999098")
        db.add_completion(self.malfoy_hp, "2021-09-15 07:56:24.999098")
        db.add_completion(self.malfoy_hp, "2021-10-02 07:56:24.999098")
        db.add_completion(self.malfoy_hp, "2021-11-17 07:56:24.999098")
        db.add_completion(self.malfoy_hp, "2021-12-30 07:56:24.999098")
        db.add_completion(self.malfoy_hp, "2022-01-30 07:56:24.999098")
        db.add_completion(self.malfoy_hp)

        db.add_completion(self.kill_voldemort_hp, "2022-01-05 07:56:24.999098")
        db.add_completion(self.kill_voldemort_hp, "2021-12-05 07:56:24.999098")

        db.add_completion(self.hedwig_hp, "2021-12-03 07:56:24.999098")

        db.add_completion(self.ginny_hp, "2021-12-21 07:56:24.999098")
        db.add_completion(self.ginny_hp)

    def create_test_data(self, database):
        """create all test data (i.e., users, habits, and habit completions) for the application

        :param database: the database connection in which the test data is to be stored ('sqlite3.connection')"""
        self.create_users(database)
        self.store_users()
        self.create_habits()
        self.store_habits()
        self.store_habit_completions()


class DataForTestingPytest(DataForTesting):
    """This class creates the test data provided by the DataForTesting class and stores it in a
    test database. The data can then be used for testing the application's main functionalities using
    pytest.

    Attributes:
        database (sqlite3.connection): the test database which stores the test data.
        additional attributes: see the documentation of the DataForTesting class
    """
    def setup_method(self):
        """create the database connection, create the test data and save it in the database"""
        self.database = db.get_db(":memory:")  # creates the database only in memory
        self.create_test_data(self.database)


class DataForTestingCLI(DataForTesting):
    """This class creates the test data provided by the DataForTesting class and stores it in the
    database specified. The data can then be used for testing the application's main functionalities at runtime
    using the CLI.

    Attributes:
        database ('sqlite3.connection'): the database which stores the test data.
        additional attributes: see the documentation of the DataForTesting class

    Parameters:
        database_name ('str'): the name of the database which stores the test data.
    """
    def __init__(self, database_name: str):
        self.database = db.get_db(database_name)
        self.create_test_data(self.database)
