import analyze as ana
import db
import test_data
from habit import HabitDB
from user import UserDB
from datetime import date, datetime, timedelta
import pytest


class TestHabitUser(test_data.DataForTestingPytest):

    def test_habit(self):
        """
        tests whether a habit object is correctly created
        """
        habit = HabitDB("Brush teeth", "weekly", "StephanieHochge", self.database)
        assert habit.name == "Brush teeth"
        assert habit.periodicity == "weekly"
        assert habit.user == "StephanieHochge"
        # TODO: Entscheidung: muss ich das überhaupt testen? (wird ja auch schon bei der Initialisierung der
        #  Testdatenbank verwendet)

    def test_user(self):
        """
        tests whether a user object is correctly created
        """
        user = UserDB("StephanieHochge", self.database)
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
        assert habit.last_completion == str(date.today())
        user2 = UserDB("Mausi", self.database)
        user2.store_user()
        habit_2 = HabitDB("Clean window", "weekly", user2, self.database)
        habit_2.store_habit()
        habit_2.check_off_habit("2021-12-05 12:54:24.999098")
        assert habit_2.last_completion == "2021-12-05"

    def test_find_last_check(self):
        assert self.teeth_sh.find_last_check() == str(date.today() - timedelta(weeks=1))

    def test_delete_habit(self):
        """test that it is possible to delete a habit and its corresponding data from the Habit and Completion tables"""
        len_completions = len(ana.create_data_frame(self.database, "Completions"))
        len_habit_data = len(ana.return_habit_completions(self.teeth_rb))
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
        self.bathroom_sh.modify_habit(name="Flat")
        assert "Flat" in ana.return_habit_names(self.user_sh)

    def test_analyze_habit(self):
        analysis_teeth = self.teeth_sh.analyze_habit()
        assert len(analysis_teeth) == 6

    def test_userDB(self):
        """
        tests whether users can be stored
        """
        user = UserDB("HansJ", self.database)
        user.store_user()

    def test_analyze_habits(self):
        habit_comparison, statistics = self.user_sh.analyze_habits()
        assert len(habit_comparison.columns) == 5
        assert "Clean bathroom" in statistics
        # TODO: Überprüfen, was passiert, wenn man keine weekly oder daily habits hat TODO: noch einen Test
        #  hinzufügen, der testet, dass bei der Summary Analyse bei der lowest completion rate richtig gerundet wird
        #  (war zuerst nicht der Fall)
