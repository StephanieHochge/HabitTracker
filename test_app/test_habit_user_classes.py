import analyze as ana
import db
import test_data
from habit import HabitDB
from user import UserDB
from datetime import date, datetime, timedelta
import pytest


class TestHabitUser(test_data.DataForTestingPytest):
    """This class tests the main functionalities provided by the application's HabitDB (habit.py) and UserDB
    (user.py) classes using the test data it inherits from the DataForTestingPytest class.

    Attributes: see the documentation of the DataForTestingPytest class
    """

    def test_habitDB(self):
        """tests whether habits can be stored and checked off and whether the last completion is calculated correctly"""
        hermione_g = UserDB("HermioneGranger", self.database)
        hermione_g.store_user()
        read = HabitDB("Read books", "daily", hermione_g)
        read.store_habit()
        read.check_off_habit()
        read.check_off_habit("2021-12-05 12:54:24.999098")
        assert read.last_completion == str(date.today())

        voldemort = UserDB("Voldemort", self.database)
        voldemort.store_user()
        kill = HabitDB("Kill Harry", "yearly", voldemort)
        kill.store_habit()
        kill.check_off_habit("2021-12-05 12:54:24.999098")
        assert kill.last_completion == "2021-12-05"

        assert self.teeth_sh.last_completion == str(date.today() - timedelta(weeks=1))

    def test_delete_habit(self):
        """test that it is possible to delete a habit and its corresponding data from the Habit and Completion tables"""
        len_completions = len(ana.create_data_frame(self.database, "Completions"))
        len_habit_data = len(ana.return_completions(self.teeth_rb))
        assert db.find_habit_id(self.teeth_rb) == 1
        self.teeth_rb.delete_habit()
        with pytest.raises(TypeError):
            db.find_habit_id(self.teeth_rb)
        len_completions_after_del = len(ana.create_data_frame(self.database, "Completions"))
        assert len_completions_after_del == (len_completions - len_habit_data)

    def test_modify_habit(self):
        self.dance_rb.modify_habit(name="Ballet", periodicity="daily")
        assert self.dance_rb.periodicity == "daily"
        assert self.dance_rb.name == "Ballet"
        assert "Ballet" in self.user_rb.habit_names
        self.bathroom_sh.modify_habit(name="Flat")
        assert "Flat" in self.user_sh.habit_names

    def test_analyze_habit(self):
        analysis_teeth = self.teeth_sh.analyze_habit()
        assert len(analysis_teeth) == 6
        assert self.teeth_sh.completion_rate == round(((6/28)*100))
        assert self.teeth_sh.current_streak == 0
        assert self.teeth_sh.breaks_total == 6
        assert self.teeth_sh.best_streak == 21

        self.bathroom_sh.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=1)))
        assert self.bathroom_sh.completion_rate == 25

        self.sleep_sh.check_off_habit(str(datetime.now() - timedelta(days=2)))
        self.sleep_sh.check_off_habit(str(datetime.now() - timedelta(days=3)))
        self.sleep_sh.check_off_habit(str(datetime.now() - timedelta(days=4)))
        assert self.sleep_sh.best_streak == 3
        assert self.sleep_sh.completion_rate == round(((3/28)*100))

    def test_userDB(self):
        """test whether users can be stored in the database"""
        user = UserDB("RonWeasley", self.database)
        user.store_user()
        user_df = ana.create_data_frame(user.database, "HabitAppUser")
        assert user.username in user_df["UserName"].to_list()

    def test_user_habits(self):
        assert self.user_sh.habit_names == ["Brush teeth", "Dance", "Clean windows", "Clean bathroom", "Go to dentist",
                                            "Sleep"]
        completed_names = [habit.name for habit in self.user_sh.completed_habits]
        assert "Sleep" not in completed_names
        assert "Brush teeth" in completed_names

    def test_return_habit_information(self):
        habit_info = self.user_sh.return_habit_information()
        assert "weekly" in habit_info["Periodicity"].to_list()
        habit_daily_info = self.user_sh.return_habit_information(periodicity="daily")
        assert "weekly" not in habit_daily_info["Periodicity"].to_list()

    def test_analyze_habits(self):
        habit_comparison, statistics = self.user_sh.analyze_habits()
        assert len(habit_comparison.columns) == 5
        assert "Clean bathroom" in statistics["Data"].to_list()
        assert self.user_sh.best_habit == "Brush teeth"
        assert self.user_sh.worst_habit == "Clean bathroom"
        assert self.user_sh.lowest_completion_rate == 0
        assert self.user_sh.longest_streak == 21

        self.conjure_hp.check_off_habit(str(datetime.now() - timedelta(days=6)))
        self.conjure_hp.check_off_habit(str(datetime.now() - timedelta(days=7)))
        self.conjure_hp.check_off_habit(str(datetime.now() - timedelta(days=8)))
        assert self.user_hp.lowest_completion_rate == round(((3/28)*100))

        # test if the lowest completion rate is calculated correctly if the user does not have any daily or
        # weekly habtis
        hulk = UserDB("Hulk", self.database)
        hulk.store_user()
        strong = HabitDB("Be strong", "monthly", hulk)
        strong.store_habit()
        assert hulk.lowest_completion_rate == "---"
        assert hulk.worst_habit == "---"

# meiner Meinung nach wurden alle wichtigen Funktionen der Habit und User Klassen getestet
