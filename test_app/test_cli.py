import datetime
from io import StringIO
from unittest.mock import patch

import main
import test_data
from user import UserDB
import analyze as ana


class TestCli(test_data.DataForTestingPytest):

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
            assert mock_stdout.getvalue() == "\x1b[0;0;41mA user with this username does not exist.\x1b[0m\n" \
                                             "\x1b[0;0;41mPlease try again.\x1b[0m\n" \
                                             "\x1b[0;0;41mA user with this username does not exist.\x1b[0m\n" \
                                             "\x1b[0;0;41mPlease try again.\x1b[0m\n" \
                                             "\x1b[0;0;41mA user with this username does not exist.\x1b[0m\n" \
                                             "\x1b[0;0;41mLogin failed three times. Do you perhaps want to perform " \
                                             "another action?\x1b[0m\n"

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

    @patch('main.input_chosen_habit', return_value="Sleep")
    def test_identify_habit(self, mock_input):
        """
        tests the identify habit function
        :return:
        """
        habit = main.identify_habit("delete", self.user_sh)
        assert habit.periodicity == "daily"
        assert habit.user == self.user_sh

    @patch('main.confirm_delete', return_value=True)
    @patch('main.input_chosen_habit', return_value="Sleep")
    def test_delete_habit(self, mock_habit, mock_confirm):
        """
        tests if the habit was successfully deleted
        :param mock_input:
        :return:
        """
        main.delete_habit(self.user_sh)
        assert "Sleep" not in ana.return_habits_only(self.user_sh)

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
        assert ana.return_habit_periodicity(self.user_sh, "Clean flat") == "monthly"

    @patch('main.input_chosen_habit', return_value="Dance")
    @patch('main.input_past_check_date', return_value="just now")
    def test_check_off_habit_now(self, mock_now, mock_habit):
        main.check_off_habit(self.user_sh)
        self.dance_sh.find_last_check()
        assert self.dance_sh.last_completion == str(datetime.date.today())

    @patch('main.input_chosen_habit', return_value="Brush teeth")
    @patch('main.input_past_check_date', return_value="yesterday")
    def test_check_off_habit_past(self, mock_check_date, mock_habit):
        main.check_off_habit(self.user_sh)
        self.teeth_sh.find_last_check()
        assert self.teeth_sh.last_completion == str(datetime.date.today() - datetime.timedelta(days=1))

    def test_determine_possible_actions(self):
        actions = {
            "no habits": ["Create habit", "Exit"],
            "habit without data": ["Manage habits", "Look at habits", "Check off habit", "Exit"],
            "habit with data": ["Manage habits", "Look at habits", "Check off habit", "Analyze habits", "Exit"]
        }
        assert main.determine_possible_actions(self.user_sh) == actions["habit with data"]
        assert main.determine_possible_actions(self.user_le) == actions["no habits"]
        assert main.determine_possible_actions(self.user_hp) == actions["habit without data"]

    # TODO: überprüfen, ob alle wichtigen Funktionen getestet wurden
    # Creating a new user:
    # test that it is not possible to store an empty value as user name
    # test that it is not possible to store a user name containing a space
    # ist nach Max nicht unbedingt notwendig, weil die eigentliche Programmlogik schon durch die Tests abgedeckt wird
