import pytest
from habit import Habit, HabitDB
import db
import os  # to be able to remove the test data base
from user import User, UserDB
import analyze as an
from datetime import date


class TestHabit:

    def setup_method(self):
        self.data_base = db.get_db("test.db")
        db.add_user(self.data_base, "StephanieHochge")
        db.add_user(self.data_base, "RajaBe")
        db.add_user(self.data_base, "LibertyEvans")
        db.add_habit(self.data_base, "RajaBe", "Brush teeth", "daily")
        db.add_habit(self.data_base, "StephanieHochge", "Brush teeth", "daily", "2021-11-30 07:54:24.999098")
        db.add_habit(self.data_base, "StephanieHochge", "Dance", "weekly", "2021-10-31 07:54:24.999098")
        db.add_habit(self.data_base, "StephanieHochge", "Clean windows", "monthly", "2021-10-31 07:54:24.999098")
        db.add_habit(self.data_base, "StephanieHochge", "Clean bathroom", "weekly", "2022-10-31 07:56:24.999098")
        db.add_habit(self.data_base, "StephanieHochge", "Go to dentist", "yearly", "2022-10-31 07:56:24.999098")
        db.add_period(self.data_base, "Brush teeth", "RajaBe")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-01")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-01")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-02")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-04")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-05")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-07")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-08")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-09")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-10")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-11")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-12")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-13")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-14")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-15")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-16")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-17")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-18")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-19")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-20")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-21")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-22")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-23")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-24")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-25")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-26")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-27")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-29")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-30")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-31")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-11-06")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-11-07")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-11-11")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-11-13")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-11-14")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-11-21")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-11-25")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-11-27")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-11-28")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-12-02")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-12-04")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-12-05")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-12-16")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-12-18")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-12-19")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-12-30")
        db.add_period(self.data_base, "Clean bathroom", "StephanieHochge", "2021-11-06")
        db.add_period(self.data_base, "Clean bathroom", "StephanieHochge", "2021-11-13")
        db.add_period(self.data_base, "Clean bathroom", "StephanieHochge", "2021-11-20")
        db.add_period(self.data_base, "Clean bathroom", "StephanieHochge", "2021-12-04")
        db.add_period(self.data_base, "Clean bathroom", "StephanieHochge", "2021-12-11")
        db.add_period(self.data_base, "Clean bathroom", "StephanieHochge", "2021-12-18")
        db.add_period(self.data_base, "Clean bathroom", "StephanieHochge", "2022-01-01")
        db.add_period(self.data_base, "Clean windows", "StephanieHochge", "2022-11-17")
        db.add_period(self.data_base, "Clean windows", "StephanieHochge", "2022-12-30")
        db.add_period(self.data_base, "Go to dentist", "StephanieHochge", "2022-12-17")
        db.add_period(self.data_base, "Go to dentist", "StephanieHochge", "2021-12-05")
        db.add_period(self.data_base, "Brush teeth", "StephanieHochge", "2021-12-03")
        db.add_period(self.data_base, "Dance", "StephanieHochge", "2021-12-21")

    def test_habit(self):
        """
        tests whether a habit object is correctly created
        """
        habit = Habit("Brush teeth", "weekly", "StephanieHochge")
        assert habit.name == "Brush teeth"
        assert habit.periodicity == "weekly"
        assert habit.user == "StephanieHochge"
        # TODO: Entscheidung: muss ich das überhaupt testen?

    def test_user(self):
        """
        tests whether a user object is correctly created
        """
        user = UserDB("StephanieHochge")
        assert user.user_name == "StephanieHochge"

    def test_user_table_db(self):
        """
        tests whether data can be added to the user table
        """
        cursor = self.data_base.cursor()  # TODO: zum Testen der Tables kann noch eine Funktion geschrieben werden (
        # Syntax wiederholt sich)
        cursor.execute("SELECT * FROM HabitAppUser")
        results = cursor.fetchall()
        assert len(results) == 3

    def test_habit_table_db(self):
        """
        tests whether data can be added to the habit table
        """
        cursor = self.data_base.cursor()
        cursor.execute("SELECT * FROM Habit")
        results = cursor.fetchall()
        assert len(results) == 6

    def test_period_table_db(self):
        """
        tests whether data can be added to the period table and whether the streak names are correctly assigned for
        each habit periodicity
        """
        cursor = self.data_base.cursor()
        cursor.execute("SELECT * FROM Period")
        results = cursor.fetchall()
        assert len(results) == 59  # test whether all records have been added successfully

        def return_streak_name(check_date, habit_id):
            cursor.execute("SELECT StreakName FROM Period WHERE CompletionDate = ? AND FKHabitID = ?",
                           (check_date, habit_id))
            return cursor.fetchone()[0]

        streak_name_daily_1 = return_streak_name("2021-12-05", 2)
        assert streak_name_daily_1 == 1
        streak_name_daily_2 = return_streak_name("2021-12-07", 2)
        assert streak_name_daily_2 == 3  # Name des Streaks gibt nicht die Anzahl der Streaks an -> es existieren
        # zwei unterschiedliche Streaks und der zweite ist mit 3 benannt

        cursor.execute("SELECT DISTINCT StreakName From Period WHERE FKHabitID = ?", [3])
        count_streaks = cursor.fetchall()
        assert len(count_streaks) == 2
        streak_name_weekly = return_streak_name("2021-12-30", 3)  # habit_id = 3 is Dance - a weekly habit
        assert streak_name_weekly == 2

        streak_name_monthly = return_streak_name("2022-12-30", 4)  # habit_id = 4 is Clean windows - a monthly habit
        assert streak_name_monthly == 1

        streak_name_yearly = return_streak_name("2022-12-17", 6)  # habit_id = 6 is Go to dentist - a yearly habit
        assert streak_name_yearly == 1

    def test_habitDB(self):
        """
        tests whether habits can be stored and checked off
        """
        habit = HabitDB("Brush teeth", "weekly", "StephanieHochge")
        habit.store_habit(self.data_base)
        habit.check_off_habit(self.data_base)
        habit.check_off_habit(self.data_base, "2021-12-05")
        assert habit.last_completion == str(date.today())
        habit_2 = HabitDB("Clean window", "weekly", "StephanieHochge")
        habit_2.store_habit(self.data_base)
        habit_2.check_off_habit(self.data_base, "2021-12-05")
        assert habit_2.last_completion == "2021-12-05"

    def test_userDB(self):
        """
        tests whether users can be stored
        """
        user = UserDB("HansJ")
        user.store_user(self.data_base)

    def test_create_data_frame(self):
        """
        tests whether data_frames can be created from data base tables
        """
        habit_df = an.create_data_frame(self.data_base, "Habit")
        user_df = an.create_data_frame(self.data_base, "HabitAppUser")
        period_df = an.create_data_frame(self.data_base, "Period")

    def test_check_for_user(self):
        """
        tests whether the function to identify whether a user name already exists works or not
        :return:
        """
        user_existing = an.check_for_user(self.data_base, "StephanieHochge")
        assert user_existing is True
        user_existing2 = an.check_for_user(self.data_base, "StephanieH")
        assert user_existing2 is False

    def test_return_habits(self):
        """
        tests whether user_habits are correctly returned
        """
        defined_habits = an.return_habits(self.data_base, "StephanieHochge")
        assert len(defined_habits) == 5

    def test_return_habits_of_type(self):
        """
        tests whether user_habits of a specific type are correctly returned
        """
        weekly_habits = an.return_habits_of_type(self.data_base, "StephanieHochge", "weekly")
        assert len(weekly_habits) == 2
        quaterly_habits = an.return_habits_of_type(self.data_base, "StephanieHochge", "quarterly")
        assert len(quaterly_habits) == 0

    def test_return_streak(self):
        # test if return_habit_id returns the correct habit_id
        habit_id = an.return_habit_id(self.data_base, "Dance", "StephanieHochge")
        assert habit_id == 3

        # test if return_habit_completions returns the correct table
        habit_completions = an.return_habit_completions(self.data_base, "Dance", "StephanieHochge")
        assert len(habit_completions) == 17

        # test if period start is correctly calculated
        period_start = an.determine_period_start("weekly", "2021-12-30")
        assert period_start == "2021-12-27"
        period_start_2 = an.determine_period_start("daily", "2021-12-30")
        assert period_start_2 == "2021-12-30"
        period_start_3 = an.determine_period_start("monthly", "2021-10-19")
        assert period_start_3 == "2021-10-01"
        period_start_4 = an.determine_period_start("yearly", "2022-12-12")
        assert period_start_4 == "2022-01-01"

        # test if the start of the next period is correctly calculated
        next_period_start = an.determine_next_period_start("daily", "2021-12-31")
        assert next_period_start == "2022-01-01"
        next_period_start_2 = an.determine_next_period_start("weekly", "2022-01-03")
        assert next_period_start_2 == "2022-01-10"
        next_period_start_3 = an.determine_next_period_start("monthly", "2021-12-03")
        assert next_period_start_3 == "2022-01-01"
        next_period_start_4 = an.determine_next_period_start("yearly", "2021-12-03")
        assert next_period_start_4 == "2022-01-01"

        # test if the start of the previous period is correctly calculated
        previous_period_start = an.determine_previous_period_start("daily", "2021-12-31")
        assert previous_period_start == "2021-12-30"
        previous_period_start_2 = an.determine_previous_period_start("weekly", "2022-01-03")
        assert previous_period_start_2 == "2021-12-27"
        previous_period_start_3 = an.determine_previous_period_start("monthly", "2021-12-01")
        assert previous_period_start_3 == "2021-11-01"
        previous_period_start_4 = an.determine_previous_period_start("yearly", "2021-01-01")
        assert previous_period_start_4 == "2020-01-01"

        # test if the longest streak of a habit is calculated correctly
        streaks = an.calculate_streak_counts(self.data_base, "Dance", "StephanieHochge")
        assert streaks.get(2) == 3

        max_streak_for_habit = an.return_longest_streak_for_habit(self.data_base, "Brush teeth", "StephanieHochge")
        assert max_streak_for_habit == 21

    def teardown_method(self):
        os.remove("test.db")  # löscht die Testdatenbank, die beim setup erstellt wurde
