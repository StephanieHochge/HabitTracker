import db
import test_data
import os


class TestDB(test_data.DataForTestingPytest):

    def test_user_table_db(self):
        """
        tests whether data can be added to the user table
        """
        cursor = self.database.cursor()  # TODO: zum Testen der Tables kann noch eine Funktion geschrieben werden (
        # Syntax wiederholt sich)
        cursor.execute("SELECT * FROM HabitAppUser")
        results = cursor.fetchall()
        assert len(results) == 4

    def test_habit_table_db(self):
        """
        tests whether data can be added to the habit table
        """
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM Habit")
        results = cursor.fetchall()
        assert len(results) == 9

    def test_completions_table_db(self):
        """
        tests whether data can be added to the period table and whether the streak names are correctly assigned for
        each habit periodicity
        """
        # TODO: testen, ob die Completions die korrekte Habit-ID haben?
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM Completions")
        results = cursor.fetchall()
        assert len(results) == 78

    def test_user_data_existing(self):
        second_database = db.get_db("test2.db")
        assert db.check_for_user_data(second_database) is False
        assert db.check_for_user_data(self.database) is True
        os.remove("test2.db")
