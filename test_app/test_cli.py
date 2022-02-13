import datetime
from io import StringIO
from unittest.mock import patch

import main
import test_data
import analyze as ana


class TestCli(test_data.DataForTestingPytest):
    """This class tests the main functionalities provided by the application's command line interface (main.py)
     using the test data it inherits from the DataForTestingPytest class.

    Attributes: see the documentation of the DataForTestingPytest class
    """

    @patch('main.input_username', return_value="Hermione")
    def test_create_new_user(self, mock_input):
        """test that it is possible to create a new user"""
        new_user = main.create_new_user(self.database)
        user_df = ana.create_data_frame(self.database, "HabitAppUser")
        assert new_user.username == "Hermione"
        assert "Hermione" in user_df["UserName"].to_list()

    @patch('sys.stdout', new_callable=StringIO)
    def test_login_fail(self, mock_stdout):
        """test that entering an unknown username leads to a failed login"""
        with patch('main.input_username', return_value="UnknownUser"):
            main.login(self.database)
            assert mock_stdout.getvalue() == "\x1b[0;0;41mA user with this username does not exist.\x1b[0m\n" \
                                             "\x1b[0;0;41mPlease try again.\x1b[0m\n" \
                                             "\x1b[0;0;41mA user with this username does not exist.\x1b[0m\n" \
                                             "\x1b[0;0;41mPlease try again.\x1b[0m\n" \
                                             "\x1b[0;0;41mA user with this username does not exist.\x1b[0m\n" \
                                             "\x1b[0;0;41mLogin failed three times. Do you perhaps want to perform " \
                                             "another action?\x1b[0m\n"

    @patch('sys.stdout', new_callable=StringIO)
    def test_login_success(self, mock_stdout):
        """test that it is possible to log in using a correct username"""
        with patch('main.input_username', return_value="StephanieHochge"):
            main.login(self.database)
            assert mock_stdout.getvalue() == "Logged in as StephanieHochge.\n"

    @patch('main.input_new_habit', return_value=("feed Hedwig", "daily"))
    def test_create_habit(self, mock_input):
        """test that it is possible to create a new habit"""
        new_habit = main.create_habit(self.user_hp)
        habit_df = ana.create_data_frame(self.database, "Habit")
        assert new_habit.name == "feed Hedwig"
        assert new_habit.periodicity == "daily"
        assert "feed Hedwig" in habit_df["Name"].to_list()

    @patch('main.input_chosen_habit', return_value="Sleep")
    def test_identify_habit(self, mock_input):
        """test that it is possible to identify the correct habit of the user"""
        habit = main.identify_habit("delete", self.user_sh)
        assert habit.periodicity == "daily"
        assert habit.user == self.user_sh

    @patch('main.confirm_delete', return_value=True)
    @patch('main.input_chosen_habit', return_value="Dance")
    def test_delete_habit(self, mock_habit, mock_confirm):
        """test if it is possible to delete a habit"""
        assert "Dance" in self.user_rb.habit_names
        main.delete_habit(self.user_rb)
        assert "Dance" not in self.user_rb.habit_names

    @patch('main.input_habit_modify_target', return_value="name")
    @patch('main.input_new_habit_name', return_value="Clean flat")
    @patch('main.input_chosen_habit', return_value="Clean bathroom")
    def test_modify_habit_name(self, mock_habit, mock_name, mock_target):
        """test if it is possible to rename a habit without changing its periodicity"""
        main.modify_habit(self.user_sh)
        assert "Clean bathroom" not in self.user_sh.habit_names

    @patch('main.input_habit_modify_target', return_value="both")
    @patch('main.input_periodicity', return_value="monthly")
    @patch('main.input_new_habit_name', return_value="Clean flat")
    @patch('main.input_chosen_habit', return_value="Clean bathroom")
    def test_modify_habit_both(self, mock_habit, mock_name, mock_periodicity, mock_target):
        """test if it possible to modify a habit's name and periodicity"""
        main.modify_habit(self.user_sh)
        habit = [habit for habit in self.user_sh.defined_habits if habit.name == "Clean flat"][0]
        assert "Clean bathroom" not in self.user_sh.habit_names
        assert habit.periodicity == "monthly"

    @patch('main.input_chosen_habit', return_value="Conjuring")
    @patch('main.input_check_day', return_value="just now")
    def test_check_off_habit_now(self, mock_now, mock_habit):
        """test that it is possible to check off a habit at the current moment"""
        main.check_off_habit(self.user_hp)
        assert self.conjure_hp.last_completion == str(datetime.date.today())

    @patch('main.input_chosen_habit', return_value="Brush teeth")
    @patch('main.input_check_day', return_value="earlier today")
    def test_check_off_habit_earlier(self, mock_now, mock_habit):
        """test that it is possible to check off a habit at the earlier today"""
        main.check_off_habit(self.user_sh)
        assert self.teeth_sh.last_completion == str(datetime.date.today())

    @patch('main.input_chosen_habit', return_value="Brush teeth")
    @patch('main.input_check_day', return_value="yesterday")
    def test_check_off_habit_past(self, mock_check_date, mock_habit):
        main.check_off_habit(self.user_sh)
        assert self.teeth_sh.last_completion == str(datetime.date.today() - datetime.timedelta(days=1))

    def test_determine_possible_actions(self):
        """test that the possible actions of a user are correctly determined"""
        actions = {
            "no habits": ["Create habit", "Exit"],
            "habit without data": ["Manage habits", "Look at habits", "Check off habit", "Exit"],
            "habit with data": ["Manage habits", "Look at habits", "Check off habit", "Analyze habits", "Exit"]
        }
        assert main.determine_possible_actions(self.user_sh) == actions["habit with data"]
        assert main.determine_possible_actions(self.user_le) == actions["no habits"]
        assert main.determine_possible_actions(self.user_hp) == actions["habit without data"]

# File wurde getestet, meiner Meinung nach wurden die wichtigsten Funktionen der CLI getestet
