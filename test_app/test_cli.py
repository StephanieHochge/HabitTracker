from io import StringIO
from unittest.mock import patch

import main
import test_data
from user import UserDB
import analyze as ana


class TestCli(test_data.TestDataPytest):

    @patch('main.input_username', return_value="Fritz")
    def test_create_new_user(self, mock_input):
        """
        tests the create new user function
        """
        new_user = main.create_new_user(self.database)
        assert new_user.username == "Fritz"
        # TODO: muss ich hier auch die validators testen?

    @patch('sys.stdout', new_callable=StringIO)
    def test_login_fail(self, mock_stdout):
        """tests that entering an unknown username leads to a failed login"""
        with patch('main.input_username', return_value="UnknownUser"):
            main.login(self.database)
            assert mock_stdout.getvalue() == "This user does not exist. Please enter a username that does.\nThis user " \
                                             "does not exist. Please enter a username that does.\nThis user does not " \
                                             "exist. Please enter a username that does.\nLogin failed three times.\n"

    @patch('sys.stdout', new_callable=StringIO)
    def test_login_success(self, mock_stdout):
        """test that it is possible to login using a correct username"""
        with patch('main.input_username', return_value="StephanieHochge"):
            main.login(self.database)
            assert mock_stdout.getvalue() == "Logged in as StephanieHochge\n"

    def test_start(self):
        """test that recursion works (i.e., correctly creating a new user, correctly creating a new habit,
        failing to login but then being asked to perform another action)"""
        pass

    @patch('main.input_new_habit', return_value=("sleeping", "daily"))
    def test_create_habit(self, mock_input):
        """
        tests the create new habit function
        """
        user = UserDB("Fritz", self.database)
        user.store_user()
        new_habit = main.create_habit(user)
        assert new_habit.name == "sleeping"
        assert new_habit.periodicity == "daily"

    @patch('main.input_chosen_habit', return_value="sleep")
    def test_identify_habit(self, mock_input):
        """
        tests the identify habit function
        :return:
        """
        habit = main.identify_habit("delete", self.user_sh)
        assert habit.periodicity == "daily"
        assert habit.user == self.user_sh

    @patch('main.input_chosen_habit', return_value="sleep")
    def test_delete_habit(self, mock_input):
        """
        tests if the habit was successfully deleted
        :param mock_input:
        :return:
        """
        main.delete_habit(self.user_sh)
        assert "sleep" not in ana.return_habits_only(self.user_sh)

    @patch('main.input_habit_modify_target', return_value="name")
    @patch('main.input_new_habit_name', return_value="Clean flat")
    @patch('main.input_chosen_habit', return_value="Clean bathroom")
    def test_modify_habit_name(self, mock_habit, mock_name, mock_target):
        main.modify_habit(self.user_sh)
        assert "Clean bathroom" not in ana.return_habits_only(self.user_sh)

    @patch('main.input_habit_modify_target', return_value="both")
    @patch('main.input_periodicity', return_value="monthly")
    @patch('main.input_new_habit_name', return_value="Clean flat")
    @patch('main.input_chosen_habit', return_value="Clean bathroom")
    def test_modify_habit_both(self, mock_habit, mock_name, mock_periodicity, mock_target):
        main.modify_habit(self.user_sh)
        assert "Clean bathroom" not in ana.return_habits_only(self.user_sh)
        assert ana.return_periodicity(self.user_sh, "Clean flat") == "monthly"

    # TODO: test user input (see main.py)
    ## Tests der CLI
    # Creating a new user:
    # test that it is not possible to store an empty value as user name
    # test that it is not possible to store a user name containing a space
    # ist nach Max nicht unbedingt notwendig, weil die eigentliche Programmlogik schon durch die Tests abgedeckt wird
