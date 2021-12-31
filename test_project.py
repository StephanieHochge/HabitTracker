import pytest
from habit import Habit, HabitDB
import db
import os  # to be able to remove the test data base
from user import User, UserDB
import analyze as an


class TestHabit:

    def setup_method(self):
        self.data_base = db.get_db("test.db")
        db.add_user(self.data_base, "StephanieHochge")
        db.add_user(self.data_base, "RajaBe")
        db.add_user(self.data_base, "LibertyEvans")
        db.add_habit(self.data_base, "RajaBe", "Brush teeth", "daily")
        db.add_habit(self.data_base, "StephanieHochge", "Brush teeth", "daily", "2021-11-30 07:54:24.999098")
        db.add_habit(self.data_base, "StephanieHochge", "Dance", "weekly", "2021-10-31 07:54:24.999098")
        db.add_habit(self.data_base, "StephanieHochge", "Clean windows", "monthly", "2021-10-31 07:54:24.999098")
        db.add_habit(self.data_base, "StephanieHochge", "Clean bathroom", "weekly", "2022-10-31 07:56:24.999098")
        db.add_habit(self.data_base, "StephanieHochge", "Go to dentist", "half yearly", "2022-10-31 07:56:24.999098")
        db.complete_habit(self.data_base, "Brush teeth", "RajaBe")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-01")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-02")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-03")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-04")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-05")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-07")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-08")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-09")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-10")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-11")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-12")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-13")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-14")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-15")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-16")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-17")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-18")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-19")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-20")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-21")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-22")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-23")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-24")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-25")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-26")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-27")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-29")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-30")
        db.complete_habit(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-31")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-11-06")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-11-07")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-11-11")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-11-13")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-11-14")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-11-21")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-11-25")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-11-27")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-11-28")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-12-02")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-12-04")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-12-05")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-12-16")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-12-18")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-12-19")
        db.complete_habit(self.data_base, "Dance", "StephanieHochge", "2021-12-30")
        db.complete_habit(self.data_base, "Clean bathroom", "StephanieHochge", "2021-11-06")
        db.complete_habit(self.data_base, "Clean bathroom", "StephanieHochge", "2021-11-13")
        db.complete_habit(self.data_base, "Clean bathroom", "StephanieHochge", "2021-11-20")
        db.complete_habit(self.data_base, "Clean bathroom", "StephanieHochge", "2021-12-04")
        db.complete_habit(self.data_base, "Clean bathroom", "StephanieHochge", "2021-12-11")
        db.complete_habit(self.data_base, "Clean bathroom", "StephanieHochge", "2021-12-18")
        db.complete_habit(self.data_base, "Clean bathroom", "StephanieHochge", "2022-01-01")
        db.complete_habit(self.data_base, "Clean windows", "StephanieHochge", "2022-11-17")
        db.complete_habit(self.data_base, "Clean windows", "StephanieHochge", "2022-12-30")
        db.complete_habit(self.data_base, "Go to dentist", "StephanieHochge", "2022-12-17")

    def test_habit(self):
        """
        tests whether a habit object is correctly created
        """
        habit = Habit("Brush teeth", "weekly", "StephanieHochge")
        assert habit.name == "Brush teeth"
        assert habit.periodicity == "weekly"
        assert habit.user == "StephanieHochge"
        # TODO: Entscheidung: muss ich das überhaupt testen?

    def test_user(self):
        """
        tests whether a user object is correctly created
        """
        user = UserDB("StephanieHochge")
        assert user.user_name == "StephanieHochge"

    def test_user_table_db(self):
        """
        tests whether data can be added to the user table
        """
        cursor = self.data_base.cursor()  # TODO: zum Testen der Tables kann noch eine Funktion geschrieben werden (
        # Syntax wiederholt sich)
        cursor.execute("SELECT * FROM HabitAppUser")
        results = cursor.fetchall()
        assert len(results) == 3

    def test_habit_table_db(self):
        """
        tests whether data can be added to the habit table
        """
        cursor = self.data_base.cursor()
        cursor.execute("SELECT * FROM Habit")
        results = cursor.fetchall()
        assert len(results) == 6

    def test_completion_table_db(self):
        """
        tests whether data can be added to the completion table
        """
        cursor = self.data_base.cursor()
        cursor.execute("SELECT * FROM Completion")
        results = cursor.fetchall()
        assert len(results) == 56

    def test_habitDB(self):
        """
        tests whether habits can be stored and checked off
        """
        habit = HabitDB("Brush teeth", "weekly", "StephanieHochge")
        habit.store_habit(self.data_base)
        habit.check_off_habit(self.data_base)

    def test_userDB(self):
        """
        tests whether users can be stored
        """
        user = UserDB("HansJ")
        user.store_user(self.data_base)

    def test_create_data_frame(self):
        """
        tests whether data_frames can be created from data base tables
        """
        habit_df = an.create_data_frame(self.data_base, "Habit")
        user_df = an.create_data_frame(self.data_base, "HabitAppUser")
        completion_df = an.create_data_frame(self.data_base, "Completion")

    def test_return_user_habits(self):
        """
        tests whether user_habits are correctly returned
        """
        defined_habits = an.return_user_habits(self.data_base, "StephanieHochge")
        assert len(defined_habits) == 5

    def teardown_method(self):
        os.remove("test.db")  # löscht die Testdatenbank, die beim setup erstellt wurde
