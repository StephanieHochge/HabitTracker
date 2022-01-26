from test_app import TestData
from habit import HabitDB
from user import UserDB


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
