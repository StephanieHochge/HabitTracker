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
        """test whether habits can be stored and checked off and whether the last completion is calculated correctly"""
        dumbledore = UserDB("Dumbledore", self.database)
        dumbledore.store_user()
        read = HabitDB("Disappear spectacularly", "daily", dumbledore)
        read.store_habit()
        read.check_off_habit()
        read.check_off_habit("2021-12-05 12:54:24.999098")
        assert read.last_completion == str(date.today())

        sirius_b = UserDB("SiriusB", self.database)
        sirius_b.store_user()
        leave = HabitDB("Leave Askaban", "yearly", sirius_b)
        leave.store_habit()
        leave.check_off_habit("2021-12-05 12:54:24.999098")
        assert leave.last_completion == "2021-12-05"

        assert self.hedwig_hp.last_completion == str(date.today() - timedelta(weeks=1))

    def test_delete_habit(self):
        """test that it is possible to delete a habit and its corresponding data from the 'Habit' and
        'Completions' tables"""
        len_completions = len(ana.create_data_frame(self.database, "Completions"))
        len_habit_data = len(ana.return_completions(self.study_hg))
        assert db.find_habit_id(self.study_hg) == 1
        self.study_hg.delete_habit()
        with pytest.raises(TypeError):
            db.find_habit_id(self.study_hg)
        len_completions_after_del = len(ana.create_data_frame(self.database, "Completions"))
        assert len_completions_after_del == (len_completions - len_habit_data)

    def test_modify_habit(self):
        """test that it is possible to modify a habit's name and/or periodicity"""
        self.books_hg.modify_habit(name="Correct Ron", periodicity="daily")
        assert self.books_hg.periodicity == "daily"
        assert self.books_hg.name == "Correct Ron"
        assert "Correct Ron" in self.hermione_g.habit_names
        self.quidditch_hp.modify_habit(name="Train Flying")
        assert "Train Flying" in self.harry_p.habit_names

    def test_analyze_habit(self):
        """test that a habit's statistics are calculated correctly"""
        analysis_hedwig = self.hedwig_hp.analyze_habit()
        assert len(analysis_hedwig) == 6
        assert self.hedwig_hp.completion_rate == round(((6 / 28) * 100))
        assert self.hedwig_hp.current_streak == 0
        assert self.hedwig_hp.breaks_total == 6
        assert self.hedwig_hp.best_streak == 21

        # some extra tests for the completion rate
        self.quidditch_hp.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=1)))
        assert self.quidditch_hp.completion_rate == 25

        self.conjure_hp.check_off_habit(str(datetime.now() - timedelta(days=2)))
        self.conjure_hp.check_off_habit(str(datetime.now() - timedelta(days=3)))
        self.conjure_hp.check_off_habit(str(datetime.now() - timedelta(days=4)))
        assert self.conjure_hp.best_streak == 3
        assert self.conjure_hp.completion_rate == round(((3 / 28) * 100))

    def test_userDB(self):
        """test whether users can be stored in the database"""
        user = UserDB("Dobby", self.database)
        user.store_user()
        user_df = ana.create_data_frame(user.database, "HabitAppUser")
        assert user.username in user_df["UserName"].to_list()

    def test_user_habits(self):
        """test whether a user's habit names and completed habits are returned correctly"""
        assert self.harry_p.habit_names == ["Feed Hedwig", "Meet Ginny", "Tease Malfoy", "Train Quidditch",
                                            "Kill Voldemort", "Conjuring"]
        completed_names = [habit.name for habit in self.harry_p.completed_habits]
        assert "Conjuring" not in completed_names
        assert "Feed Hedwig" in completed_names

    def test_return_habit_information(self):
        """test wehther habit information can be returned correctly for all habits and for habits with
        a certain periodicity"""
        habit_info = self.harry_p.return_habit_information()
        assert "weekly" in habit_info["Periodicity"].to_list()
        habit_daily_info = self.harry_p.return_habit_information(periodicity="daily")
        assert "weekly" not in habit_daily_info["Periodicity"].to_list()

    def test_analyze_habits(self):
        """test if a user's statistics are calculated correctly"""
        habit_comparison, statistics = self.harry_p.analyze_habits()
        assert len(habit_comparison.columns) == 5
        assert "Train Quidditch" in statistics["Data"].to_list()
        assert self.harry_p.best_habit == "Feed Hedwig"
        assert self.harry_p.worst_habit == "Train Quidditch"
        assert self.harry_p.lowest_completion_rate == 0
        assert self.harry_p.longest_streak == 21

        # test the calculation of the lowest completion rate
        self.kill_harry_v.check_off_habit(str(datetime.now() - timedelta(days=6)))
        self.kill_harry_v.check_off_habit(str(datetime.now() - timedelta(days=7)))
        self.kill_harry_v.check_off_habit(str(datetime.now() - timedelta(days=8)))
        assert self.voldemort.lowest_completion_rate == round(((3 / 28) * 100))

        # test if the lowest completion rate is calculated correctly if the user does not have any daily or
        # weekly habtis
        hulk = UserDB("Hulk", self.database)
        hulk.store_user()
        strong = HabitDB("Be strong", "monthly", hulk)
        strong.store_habit()
        assert hulk.lowest_completion_rate == "---"
        assert hulk.worst_habit == "---"
