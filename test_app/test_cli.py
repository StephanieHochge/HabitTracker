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

    @patch('main.input_username', return_value="Dumbledore")
    def test_create_new_user(self, mock_input):
        """test that it is possible to create a new user"""
        new_user = main.create_new_user(self.database)
        user_df = ana.create_data_frame(self.database, "HabitAppUser")
        assert new_user.username == "Dumbledore"
        assert "Dumbledore" in user_df["UserName"].to_list()

    @patch('sys.stdout', new_callable=StringIO)
    def test_login_fail(self, mock_stdout):
        """test that entering an unknown username results in a failed login"""
        with patch('main.input_username', return_value="UnknownUser"):
            main.login(self.database)
            assert mock_stdout.getvalue() == "A user with this username does not exist.\n" \
                                             "Please try again.\n" \
                                             "A user with this username does not exist.\n" \
                                             "Please try again.\n" \
                                             "A user with this username does not exist.\n" \
                                             "Login failed three times. Do you perhaps want to perform " \
                                             "another action?\n"

    @patch('sys.stdout', new_callable=StringIO)
    def test_login_success(self, mock_stdout):
        """test that it is possible to log in using a correct username"""
        with patch('main.input_username', return_value="HarryP"):
            main.login(self.database)
            assert mock_stdout.getvalue() == "Logged in as HarryP.\n"

    @patch('main.input_new_habit', return_value=("Fight", "daily"))
    def test_create_habit(self, mock_input):
        """test that it is possible to create a new habit"""
        new_habit = main.create_habit(self.voldemort)
        habit_df = ana.create_data_frame(self.database, "Habit")
        assert new_habit.name == "Fight"
        assert new_habit.periodicity == "daily"
        assert "Fight" in habit_df["Name"].to_list()

    @patch('main.input_chosen_habit', return_value="Conjuring")
    def test_identify_habit(self, mock_input):
        """test that it is possible to identify the correct habit of the user"""
        habit = main.identify_habit("delete", self.harry_p)
        assert habit.periodicity == "daily"
        assert habit.user == self.harry_p

    @patch('main.confirm_delete', return_value=True)
    @patch('main.input_chosen_habit', return_value="Read books")
    def test_delete_habit(self, mock_habit, mock_confirm):
        """test if it is possible to delete a habit"""
        assert "Read books" in self.hermione_g.habit_names
        main.delete_habit(self.hermione_g)
        assert "Read books" not in self.hermione_g.habit_names

    @patch('main.input_habit_modify_target', return_value="name")
    @patch('main.input_new_habit_name', return_value="Kill Tom Riddle")
    @patch('main.input_chosen_habit', return_value="Kill Voldemort")
    def test_modify_habit_name(self, mock_habit, mock_name, mock_target):
        """test if it is possible to rename a habit without changing its periodicity"""
        assert self.kill_voldemort_hp.periodicity == "yearly"
        main.modify_habit(self.harry_p)
        assert "Kill Voldemort" not in self.harry_p.habit_names
        assert "Kill Tom Riddle" in self.harry_p.habit_names
        assert self.kill_voldemort_hp.periodicity == "yearly"

    @patch('main.input_habit_modify_target', return_value="both")
    @patch('main.input_periodicity', return_value="monthly")
    @patch('main.input_new_habit_name', return_value="Kill Tom Riddle")
    @patch('main.input_chosen_habit', return_value="Kill Voldemort")
    def test_modify_habit_both(self, mock_habit, mock_name, mock_periodicity, mock_target):
        """test if it possible to modify a habit's name and periodicity"""
        main.modify_habit(self.harry_p)
        habit = [habit for habit in self.harry_p.defined_habits if habit.name == "Kill Tom Riddle"][0]
        assert "Kill Voldemort" not in self.harry_p.habit_names
        assert habit.periodicity == "monthly"

    @patch('main.input_chosen_habit', return_value="Kill Harry")
    @patch('main.input_check_day', return_value="just now")
    def test_check_off_habit_now(self, mock_now, mock_habit):
        """test that it is possible to check off a habit with the current moment as time of check off"""
        main.check_off_habit(self.voldemort)
        assert self.kill_harry_v.last_completion == str(datetime.date.today())

    @patch('main.input_chosen_habit', return_value="Feed Hedwig")
    @patch('main.input_check_day', return_value="earlier today")
    def test_check_off_habit_earlier(self, mock_now, mock_habit):
        """test that it is possible to check off a habit with 'earlier today' as time of check off"""
        main.check_off_habit(self.harry_p)
        assert self.hedwig_hp.last_completion == str(datetime.date.today())

    @patch('main.input_chosen_habit', return_value="Feed Hedwig")
    @patch('main.input_check_day', return_value="yesterday")
    def test_check_off_habit_past(self, mock_check_date, mock_habit):
        """test that it is possible to check off a habit with yesterday as time of check off"""
        main.check_off_habit(self.harry_p)
        assert self.hedwig_hp.last_completion == str(datetime.date.today() - datetime.timedelta(days=1))

    def test_determine_possible_actions(self):
        """test that the possible actions of a user are determined correctly"""
        actions = {
            "no habits": ["Create habit", "Exit"],
            "habit without data": ["Manage habits", "Look at habits", "Check off habit", "Exit"],
            "habit with data": ["Manage habits", "Look at habits", "Check off habit", "Analyze habits", "Exit"]
        }
        assert main.determine_possible_actions(self.harry_p) == actions["habit with data"]
        assert main.determine_possible_actions(self.ron_w) == actions["no habits"]
        assert main.determine_possible_actions(self.voldemort) == actions["habit without data"]
