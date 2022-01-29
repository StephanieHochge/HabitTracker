import analyze as ana
import db
from test_app import TestData
from habit import HabitDB
from user import UserDB
from datetime import date, datetime, timedelta
import pytest


class TestHabitUser(TestData):

    def test_habit(self):
        """
        tests whether a habit object is correctly created
        """
        habit = HabitDB("Brush teeth", "weekly", "StephanieHochge")
        assert habit.name == "Brush teeth"
        assert habit.periodicity == "weekly"
        assert habit.user == "StephanieHochge"
        # TODO: Entscheidung: muss ich das überhaupt testen? (wird ja auch schon bei der Initialisierung der
        #  Testdatenbank verwendet)

    def test_user(self):
        """
        tests whether a user object is correctly created
        """
        user = UserDB("StephanieHochge")
        assert user.username == "StephanieHochge"

    def test_habitDB(self):
        """
        tests whether habits can be stored and checked off
        """
        user = UserDB("Hansi", self.database)
        user.store_user()
        habit = HabitDB("Brush teeth", "weekly", user, self.database)
        habit.store_habit()
        habit.check_off_habit()
        habit.check_off_habit("2021-12-05 12:54:24.999098")
        last_completion_date, _ = habit.last_completion.split(" ")
        assert last_completion_date == str(date.today())
        user2 = UserDB("Mausi", self.database)
        user2.store_user()
        habit_2 = HabitDB("Clean window", "weekly", user2, self.database)
        habit_2.store_habit()
        habit_2.check_off_habit("2021-12-05 12:54:24.999098")
        last_completion_date_2, _ = habit_2.last_completion.split(" ")
        assert last_completion_date_2 == "2021-12-05"

    def test_find_last_check(self):
        assert self.teeth_sh.find_last_check() == str(date.today() - timedelta(weeks=1))

    def test_delete_habit(self):
        assert db.find_habit_id(self.teeth_rb) == 1
        assert self.teeth_rb.delete_habit() is True
        with pytest.raises(TypeError):
            db.find_habit_id(self.teeth_rb)
        with pytest.raises(IndexError):  # test if corresponding data in completions was also deleted
            ana.return_habit_completions(self.teeth_rb)

    def test_modify_habit(self):
        assert self.dance_rb.modify_habit(name="Ballet", periodicity="daily") is True
        assert self.dance_rb.periodicity == "daily"
        assert self.dance_rb.name == "Ballet"
        assert self.bathroom_sh.modify_habit(name="Flat") is True
        assert "Flat" in ana.return_habits_only(self.user_sh)

    def test_analyze_habit(self):
        analysis_teeth = self.teeth_sh.analyze_habit()
        assert len(analysis_teeth) == 6

    def test_userDB(self):
        """
        tests whether users can be stored
        """
        user = UserDB("HansJ", self.database)
        user.store_user()
