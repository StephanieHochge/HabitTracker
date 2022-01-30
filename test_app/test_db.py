import db
import test_data


class TestDB(test_data.TestDataPytest):

    def test_user_table_db(self):
        """
        tests whether data can be added to the user table
        """
        cursor = self.database.cursor()  # TODO: zum Testen der Tables kann noch eine Funktion geschrieben werden (
        # Syntax wiederholt sich)
        cursor.execute("SELECT * FROM HabitAppUser")
        results = cursor.fetchall()
        assert len(results) == 3

    def test_habit_table_db(self):
        """
        tests whether data can be added to the habit table
        """
        cursor = self.database.cursor()
        cursor.execute("SELECT * FROM Habit")
        results = cursor.fetchall()
        assert len(results) == 8

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
        assert len(db.user_data_existing(second_database)) == 0
        assert len(db.user_data_existing(self.database)) > 0
