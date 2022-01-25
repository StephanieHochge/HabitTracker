import db
from user import UserDB
from habit import HabitDB
from datetime import date, datetime
import os
import analyze_V2 as ana


class TestHabitAnalysis:

    def setup_method(self):
        self.database = db.get_db("test.db")
        self.user_sh = UserDB("StephanieHochge", self.database)
        self.user_rb = UserDB("RajaBe", self.database)
        self.user_le = UserDB("LibertyEvans", self.database)
        db.add_user(self.user_sh)
        db.add_user(self.user_rb)
        db.add_user(self.user_le)
        self.teeth_rb = HabitDB("Brush teeth", "daily", self.user_rb, self.database)
        self.teeth_sh = HabitDB("Brush teeth", "daily", self.user_sh, self.database)
        self.dance_sh = HabitDB("Dance", "weekly", self.user_sh, self.database)
        self.windows_sh = HabitDB("Clean windows", "monthly", self.user_sh, self.database)
        self.bathroom_sh = HabitDB("Clean bathroom", "weekly", self.user_sh, self.database)
        self.dentist_sh = HabitDB("Go to dentist", "yearly", self.user_sh, self.database)
        db.add_habit(self.teeth_rb)
        db.add_habit(self.teeth_sh, "2021-11-30 07:54:24.999098")
        db.add_habit(self.dance_sh, "2021-10-31 07:54:24.999098")
        db.add_habit(self.windows_sh, "2021-10-31 07:54:24.999098")
        db.add_habit(self.bathroom_sh, "2022-10-31 07:56:24.999098")
        db.add_habit(self.dentist_sh, "2022-10-31 07:56:24.999098")
        db.add_period(self.teeth_rb)
        db.add_period(self.teeth_sh, "2021-12-01")
        db.add_period(self.teeth_sh, "2021-12-01")
        db.add_period(self.teeth_sh, "2021-12-02")
        db.add_period(self.teeth_sh, "2021-12-02")
        db.add_period(self.teeth_sh, "2021-12-02")
        db.add_period(self.teeth_sh, "2021-12-04")
        db.add_period(self.teeth_sh, "2021-12-05")
        db.add_period(self.teeth_sh, "2021-12-07")
        db.add_period(self.teeth_sh, "2021-12-08")
        db.add_period(self.teeth_sh, "2021-12-09")
        db.add_period(self.teeth_sh, "2021-12-10")
        db.add_period(self.teeth_sh, "2021-12-11")
        db.add_period(self.teeth_sh, "2021-12-12")
        db.add_period(self.teeth_sh, "2021-12-13")
        db.add_period(self.teeth_sh, "2021-12-14")
        db.add_period(self.teeth_sh, "2021-12-15")
        db.add_period(self.teeth_sh, "2021-12-16")
        db.add_period(self.teeth_sh, "2021-12-17")
        db.add_period(self.teeth_sh, "2021-12-18")
        db.add_period(self.teeth_sh, "2021-12-19")
        db.add_period(self.teeth_sh, "2021-12-20")
        db.add_period(self.teeth_sh, "2021-12-21")
        db.add_period(self.teeth_sh, "2021-12-22")
        db.add_period(self.teeth_sh, "2021-12-23")
        db.add_period(self.teeth_sh, "2021-12-24")
        db.add_period(self.teeth_sh, "2021-12-25")
        db.add_period(self.teeth_sh, "2021-12-26")
        db.add_period(self.teeth_sh, "2021-12-27")
        db.add_period(self.teeth_sh, "2021-12-29")
        db.add_period(self.teeth_sh, "2021-12-30")
        db.add_period(self.teeth_sh, "2021-12-31")
        db.add_period(self.dance_sh, "2021-11-06")
        db.add_period(self.dance_sh, "2021-11-07")
        db.add_period(self.dance_sh, "2021-11-11")
        db.add_period(self.dance_sh, "2021-11-13")
        db.add_period(self.dance_sh, "2021-11-14")
        db.add_period(self.dance_sh, "2021-11-21")
        db.add_period(self.dance_sh, "2021-11-25")
        db.add_period(self.dance_sh, "2021-11-27")
        db.add_period(self.dance_sh, "2021-11-28")
        db.add_period(self.dance_sh, "2021-12-02")
        db.add_period(self.dance_sh, "2021-12-04")
        db.add_period(self.dance_sh, "2021-12-05")
        db.add_period(self.dance_sh, "2021-12-16")
        db.add_period(self.dance_sh, "2021-12-18")
        db.add_period(self.dance_sh, "2021-12-19")
        db.add_period(self.dance_sh, "2021-12-30")
        db.add_period(self.bathroom_sh, "2021-11-06")
        db.add_period(self.bathroom_sh, "2021-11-13")
        db.add_period(self.bathroom_sh, "2021-11-20")
        db.add_period(self.bathroom_sh, "2021-12-04")
        db.add_period(self.bathroom_sh, "2021-12-11")
        db.add_period(self.bathroom_sh, "2021-12-18")
        db.add_period(self.bathroom_sh, "2022-01-01")
        db.add_period(self.windows_sh, "2021-06-23")
        db.add_period(self.windows_sh, "2021-07-06")
        db.add_period(self.windows_sh, "2021-09-15")
        db.add_period(self.windows_sh, "2021-10-02")
        db.add_period(self.windows_sh, "2021-11-17")
        db.add_period(self.windows_sh, "2021-12-30")
        db.add_period(self.windows_sh)
        db.add_period(self.dentist_sh, "2022-12-17")
        db.add_period(self.dentist_sh, "2021-12-05")
        db.add_period(self.teeth_sh, "2021-12-03")
        db.add_period(self.dance_sh, "2021-12-21")
        db.add_period(self.dance_sh)

    # TODO: die Datenbank noch in einer Überklasse speichern, damit die von den Unterklassen auch verwendet werden kann

    def test_calculate_period_starts(self):
        """
        tests if the period starts are correctly calculated
        """
        # test weekly_start, monthly_start and yearly_start functions
        assert ana.weekly_start(date(2022, 1, 26)) == date(2022, 1, 24)
        assert ana.monthly_start(date(2022, 2, 26)) == date(2022, 2, 1)
        assert ana.yearly_start(date(2022, 3, 24)) == date(2022, 1, 1)

        # test calculate_one_period_start function
        assert ana.calculate_one_period_start("weekly", date(2022, 1, 26)) == date(2022, 1, 24)
        assert ana.calculate_one_period_start("daily", date(2022, 2, 23)) == date(2022, 2, 23)
        assert ana.calculate_one_period_start("monthly", date(2021, 12, 24)) == date(2021, 12, 1)
        assert ana.calculate_one_period_start("yearly", date(2021, 8, 2)) == date(2021, 1, 1)

        # test calculate_period_starts function
        check_dates_daily = ["2022-01-25", "2022-01-27"]
        periods_daily = ana.calculate_period_starts("daily", check_dates_daily)
        assert periods_daily == [date(2022, 1, 25), date(2022, 1, 27)]

        check_dates_weekly = [date(2022, 1, 25), date(2022, 1, 20), date(2022, 1, 26)]
        periods_weekly = ana.calculate_period_starts("weekly", check_dates_weekly)
        assert periods_weekly == [date(2022, 1, 24), date(2022, 1, 17), date(2022, 1, 24)]

        check_dates_monthly = ["2022-01-15", "2021-12-14"]
        periods_monthly = ana.calculate_period_starts("monthly", check_dates_monthly)
        assert periods_monthly == [date(2022, 1, 1), date(2021, 12, 1)]

        check_dates_yearly = [date(2021, 6, 1), date(2020, 5, 30)]
        periods_yearly = ana.calculate_period_starts("yearly", check_dates_yearly)
        assert periods_yearly == [date(2021, 1, 1), date(2020, 1, 1)]

        # test tidy_starts function
        tidy_starts_weekly = ana.tidy_starts(periods_weekly)
        assert tidy_starts_weekly == [date(2022, 1, 17), date(2022, 1, 24)]

        # test add_future_period function
        # wird nur einmal getestet, weil calculate_one_period_start schon getestet wurde
        assert ana.add_future_period(tidy_starts_weekly, "weekly") == [date(2022, 1, 17), date(2022, 1, 24),
                                                                       date(2022, 2, 7)]

        # test return_final_period_starts function
        final_periods_teeth = ana.return_final_period_starts(self.teeth_sh)
        final_periods_dance = ana.return_final_period_starts(self.dance_sh)
        final_periods_windows = ana.return_final_period_starts(self.windows_sh)
        final_periods_dentist = ana.return_final_period_starts(self.dentist_sh)
        assert len(final_periods_teeth) == 30
        assert len(final_periods_dance) == 10
        assert len(final_periods_windows) == 8
        assert len(final_periods_dentist) == 3


    def teardown_method(self):
        os.remove("test.db")  # löscht die Testdatenbank, die beim setup erstellt wurde
