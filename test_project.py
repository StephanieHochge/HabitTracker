import pytest
from habit import Habit
import db
import os  # to be able to remove the test data base


class TestHabit:

    def setup_method(self):
        self.data_base = db.get_db("test.db")
        db.add_user(self.data_base, "StephanieHochge")
        db.add_user(self.data_base, "RajaBe")
        db.add_user(self.data_base, "LibertyEvans")
        # TODO: Insert further test data into test database

    def test_habit(self):
        """
        tests whether a habit object is correctly created
        """
        habit = Habit("Brush teeth", "weekly", "StephanieHochge")
        assert habit.name == "Brush teeth"
        assert habit.periodicity == "weekly"
        assert habit.user == "StephanieHochge"
        # TODO: Entscheidung: muss ich das überhaupt testen?

    def test_user_table_db(self):
        """
        tests whether data can be added to the user_table
        """
        cursor = self.data_base.cursor()
        cursor.execute("SELECT * FROM HabitAppUser")  # TODO: noch in eine Funktion packen
        results = cursor.fetchall()
        assert len(results) == 3

    def test_habit_table_db(self):
        """
        tests whether a habit can be correctly inserted into the habit table of the db
        """
        pass

    def teardown_method(self):
        os.remove("test.db")  # löscht die Testdatenbank, die beim setup erstellt wurde
