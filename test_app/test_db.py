import db
import test_data
import os


class TestDB(test_data.DataForTestingPytest):
    """This class tests the main functionalities provided by the application's database module (db.py)
    using the test data it inherits from the DataForTestingPytest class.

    Attributes: see the documentation of the DataForTestingPytest class
    """

    def retrieve_data(self, table):
        """retrieve all data of a table

        :param table: the name of the table (type: str)
        :return: the data stored in the table (type: list of tuples)
        """
        cursor = self.database.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        return cursor.fetchall()

    def test_user_table_db(self):
        """test whether data was added to the HabitAppUser table"""
        assert len(self.retrieve_data("HabitAppUser")) == 4

    def test_find_user_id(self):
        """test whether the correct user ID is returned"""
        assert db.find_user_id(self.user_sh) == 1
        assert db.find_user_id(self.user_hp) == 4

    def test_find_habit_id(self):
        """test whether the correct habit ID is returned"""
        assert db.find_habit_id(self.teeth_rb) == 1
        assert db.find_habit_id(self.dance_sh) == 4

    def test_habit_table_db(self):
        """test whether data was added to the habit table and whether they have the correct user_id"""
        assert len(self.retrieve_data("Habit")) == 9
        cursor = self.database.cursor()  # look for the user_id of a habit
        cursor.execute("SELECT FKUserID FROM Habit WHERE Name = ? AND PKHabitID = ?",
                       ("Conjuring", 9))
        user_id = cursor.fetchone()[0]
        assert user_id == 4

    def test_completions_table_db(self):
        """test whether data was added to the completions table"""
        assert len(self.retrieve_data("Completions")) == 79
        cursor = self.database.cursor()  # look for the user_id of a habit
        cursor.execute("SELECT FKHabitID FROM Completions WHERE CompletionDate = ? AND PKCompletionsID = ?",
                       ("2021-12-01", 5))
        habit_id = cursor.fetchone()[0]
        assert habit_id == 3

    def test_user_data_existing(self):
        """test whether it is possible to check if user data is already existing"""
        second_database = db.get_db("test2.db")
        assert db.check_for_user_data(second_database) is False
        assert db.check_for_user_data(self.database) is True
        os.remove("test2.db")


# File wurde getestet, meiner Meinung nach wurden die wichtigsten Funktionen der database getestet
