from datetime import date, timedelta, datetime

import analyze as ana
import test_data
from user import UserDB


class TestHabitAnalysis(test_data.DataForTestingPytest):

    def test_create_data_frame(self):
        """test whether dataframes can be created from database tables"""
        habit_df = ana.create_data_frame(self.database, "Habit")
        assert len(habit_df) == 9
        user_df = ana.create_data_frame(self.database, "HabitAppUser")
        assert len(user_df) == 4
        completions_df = ana.create_data_frame(self.database, "Completions")
        assert len(completions_df) == 79

    def test_check_for_username(self):
        """test whether the database can be checked for the assistance of usernames"""
        user_existing = ana.check_for_username(self.user_sh)
        assert user_existing is True
        user_sh_2 = UserDB("StephanieH", self.database)
        user_existing_2 = ana.check_for_username(user_sh_2)
        assert user_existing_2 is False

    def test_show_habit_data(self):
        """test whether a user's habit information is returned correctly"""
        defined_habits = ana.show_habit_data(self.user_sh)
        assert len(defined_habits) == 6
        assert "Sleep" in defined_habits["Name"].to_list()

    def test_return_completions(self):
        """test if a habit's completion dates are correctly returned"""
        habit_completions_dance_sh = ana.return_completions(self.dance_sh)
        assert len(habit_completions_dance_sh) == 20
        habit_completions_dance_rb = ana.return_completions(self.dance_rb)
        assert habit_completions_dance_rb == ["2021-12-02", "2021-12-31"]

    def test_check_any_completions(self):
        """test if it is possible to check whether the user has completed any habits"""
        completions_sh = ana.return_all_completions(self.user_sh)
        completions_le = ana.return_all_completions(self.user_le)
        assert len(completions_sh) == 6
        assert len(completions_le) == 0
        assert ana.check_any_completions(self.user_sh) is True
        assert ana.check_any_completions(self.user_le) is False

    def test_return_periodicity(self):
        """test whether the periodicity of the habit is correctly returned"""
        periodicity = ana.return_periodicity(self.user_sh, "Brush teeth")
        assert periodicity == "daily"
        periodicity = ana.return_periodicity(self.user_sh, "Dance")
        assert periodicity == "weekly"

    def test_return_ordered_periodicities(self):
        """test whether the periodicities of a user's habits are correctly returned and in the correct order"""
        assert ana.return_ordered_periodicities(self.user_sh) == ["daily", "weekly", "monthly", "yearly"]
        assert ana.return_ordered_periodicities(self.user_rb) == ["daily", "weekly"]
        assert ana.return_ordered_periodicities(self.user_le) == []
        assert ana.return_ordered_periodicities(self.user_hp) == ["daily"]

    def test_return_habit_info(self):
        all_habits = ana.return_habit_info(self.user_sh)
        assert len(all_habits) == 6
        weekly_habits = ana.return_habit_info(self.user_sh, "weekly")
        assert len(weekly_habits) == 2
        quaterly_habits = ana.return_habit_info(self.user_sh, "quarterly")
        assert len(quaterly_habits) == 0

    def test_calculate_period_starts(self):
        """tests if the period starts corresponding to the completion dates of a habit are calculated correctly"""
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
        future_period = ana.calculate_one_period_start("weekly", date.today() + timedelta(weeks=2))
        assert ana.add_future_period(tidy_starts_weekly, "weekly") == [date(2022, 1, 17), date(2022, 1, 24),
                                                                       future_period]

        # test return_final_period_starts function
        final_periods_teeth = ana.return_final_period_starts(self.teeth_sh)
        final_periods_dance = ana.return_final_period_starts(self.dance_sh)
        final_periods_windows = ana.return_final_period_starts(self.windows_sh)
        final_periods_dentist = ana.return_final_period_starts(self.dentist_sh)
        assert len(final_periods_teeth) == 36
        assert len(final_periods_dance) == 12
        assert len(final_periods_windows) == 9
        assert len(final_periods_dentist) == 3

    def test_calculate_break_indices(self):
        """test if it is possible to correctly calculate a habit's break indices"""
        # test calculate_element_diffs function
        dates = [date(2021, 7, 3), date(2021, 7, 9), date(2021, 7, 10), date(2021, 8, 10)]
        assert ana.calculate_element_diffs(dates) == [timedelta(days=6), timedelta(days=1), timedelta(days=31)]

        # test calculate break_indices function
        final_periods_teeth = ana.return_final_period_starts(self.teeth_sh)
        final_periods_dance = ana.return_final_period_starts(self.dance_sh)
        final_periods_windows = ana.return_final_period_starts(self.windows_sh)
        final_periods_dentist = ana.return_final_period_starts(self.dentist_sh)
        assert ana.calculate_break_indices(final_periods_teeth, "daily") == [4, 25, 28, 29, 32, 34]
        assert ana.calculate_break_indices(final_periods_dance, "weekly") == [4, 7, 10]
        assert ana.calculate_break_indices(final_periods_windows, "monthly") == [1, 7]
        assert ana.calculate_break_indices(final_periods_dentist, "yearly") == [1]

    def test_calculate_longest_streak(self):
        """test if the a habit's longest streak is calculated correctly"""
        # test calculate_streak_lengths function
        assert ana.calculate_streak_lengths(self.teeth_sh) == [5, 21, 3, 1, 3, 2]
        assert ana.calculate_streak_lengths(self.dance_sh) == [5, 3, 3]
        assert ana.calculate_streak_lengths(self.windows_sh) == [2, 6]
        assert ana.calculate_streak_lengths(self.dentist_sh) == [2]

        # test calculate_longest_streak function
        assert ana.calculate_longest_streak(self.teeth_sh) == 21
        assert ana.calculate_longest_streak(self.dentist_sh) == 2

    def test_calculate_longest_streak_of_all(self):
        """test if the longest streak of all habits of a user is correctly calculated"""
        # test habit creator function
        habits_sh = ana.habit_creator(self.user_sh)
        assert len(habits_sh) == 6
        habits_rb = ana.habit_creator(self.user_rb)
        assert len(habits_rb) == 2
        habits_le = ana.habit_creator(self.user_le)
        assert len(habits_le) == 0

        # test find_completed_habits function
        habits_sh_data = ana.find_completed_habits(habits_sh)
        assert len(habits_sh_data) == 5
        habits_rb_data = ana.find_completed_habits(habits_rb)
        assert len(habits_rb_data) == 2
        habits_le_data = ana.find_completed_habits(habits_le)
        assert len(habits_le_data) == 0

        # test calculate_longest_streak_per_habit function
        longest_streaks_sh = ana.calculate_longest_streak_per_habit(habits_sh_data)
        assert longest_streaks_sh["Dance"] == 5
        longest_streak_rb = ana.calculate_longest_streak_per_habit(habits_rb_data)
        assert longest_streak_rb["Brush teeth"] == 1
        longest_streak_le = ana.calculate_longest_streak_per_habit(habits_le_data)
        assert longest_streak_le is None

        # test calculate_longest_streak_of_all function
        longest_streak_all_sh = ana.calculate_longest_streak_of_all(habits_sh_data)
        assert longest_streak_all_sh == (21, ["Brush teeth"])
        longest_streak_all_rb = ana.calculate_longest_streak_of_all(habits_rb_data)
        assert longest_streak_all_rb == (1, ["Brush teeth", "Dance"])
        longest_streak_all_le = ana.calculate_longest_streak_of_all(habits_le_data)
        assert longest_streak_all_le == (None, None)

    def test_completed_in_period(self):
        """test if it is possible to check if a habit was completed in the current or the previous period"""
        final_periods_teeth_sh = ana.return_final_period_starts(self.teeth_sh)
        final_periods_dance_sh = ana.return_final_period_starts(self.dance_sh)
        final_periods_teeth_rb = ana.return_final_period_starts(self.teeth_rb)
        assert ana.completed_in_period(final_periods_teeth_sh, self.teeth_sh.periodicity, "previous") is False
        assert ana.completed_in_period(final_periods_dance_sh, self.dance_sh.periodicity, "previous") is True
        assert ana.completed_in_period(final_periods_teeth_rb, self.teeth_rb.periodicity, "previous") is False
        assert ana.completed_in_period(final_periods_teeth_sh, self.teeth_sh.periodicity, "current") is False
        assert ana.completed_in_period(final_periods_dance_sh, self.dance_sh.periodicity, "current") is True
        assert ana.completed_in_period(final_periods_teeth_rb, self.teeth_rb.periodicity, "current") is True

    def test_calculate_curr_streak(self):
        """test if a habit's current streak is calculated correctly"""
        assert ana.calculate_curr_streak(self.teeth_sh) == 0
        assert ana.calculate_curr_streak(self.dance_sh) == 3
        assert ana.calculate_curr_streak(self.dance_rb) == 0
        self.dance_rb.check_off_habit(check_date=str(datetime.now()))
        assert ana.calculate_curr_streak(self.dance_rb) == 1
        assert ana.calculate_curr_streak(self.windows_sh) == 6

    def test_calculate_completion_rate(self):
        """test if a habit's completion rate is calculated correctly (only daily & weekly habits)"""
        assert ana.calculate_completion_rate(self.teeth_sh) == 6 / 28
        assert ana.calculate_completion_rate(self.dance_sh) == 2 / 4
        self.dance_sh.check_off_habit(str(datetime.now()-timedelta(weeks=3)))
        self.dance_sh.check_off_habit(str(datetime.now()-timedelta(weeks=4)))
        assert ana.calculate_completion_rate(self.dance_sh) == 4/4

    def test_calculate_break_no(self):
        """test if the number of breaks is calculated correctly"""
        assert ana.calculate_break_no(self.teeth_sh) == 6
        assert ana.calculate_break_no(self.dance_sh) == 2
        assert ana.calculate_break_no(self.windows_sh) == 1
        assert ana.calculate_break_no(self.dentist_sh) == 0
        self.sleep_sh.check_off_habit(str(datetime.now() - timedelta(days=1)))
        assert ana.calculate_break_no(self.sleep_sh) == 0

    def test_calculate_worst_completion_rate_of_all(self):
        """test if a user's lowest completion rate and the corresponding habit(s) are correctly determined"""

        # test if completions rates per habit are correctly calculated
        self.dance_rb.check_off_habit(str(datetime.now() - timedelta(weeks=1)))
        self.teeth_rb.check_off_habit(str(datetime.now() - timedelta(weeks=1)))
        self.teeth_rb.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=1)))
        self.teeth_rb.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=2)))
        self.teeth_rb.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=3)))
        self.teeth_rb.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=4)))
        self.teeth_rb.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=5)))
        self.teeth_rb.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=6)))

        completed_habits_sh = self.user_sh.completed_habits
        completed_habits_rb = self.user_rb.completed_habits

        completion_rates_sh = ana.calculate_completion_rate_per_habit(completed_habits_sh)
        assert list(completion_rates_sh.values()) == [6 / 28, 2 / 4, 0 / 4]
        completion_rates_rb = ana.calculate_completion_rate_per_habit(completed_habits_rb)
        assert list(completion_rates_rb.values()) == [7 / 28, 1 / 4]

        # test if the lowest completion rate and the corresponding habit is correctly identified
        lowest_completion_rate_sh, worst_habit_sh = ana.calculate_worst_completion_rate_of_all(completed_habits_sh)
        assert round(lowest_completion_rate_sh) == 0
        assert worst_habit_sh == ["Clean bathroom"]
        lowest_completion_rate_rb, worst_habit_rb = ana.calculate_worst_completion_rate_of_all(completed_habits_rb)
        assert lowest_completion_rate_rb == 0.25
        assert worst_habit_rb == ["Brush teeth", "Dance"]

    def test_analyze_all_habits(self):
        """test if the dataframes to analyze all habits are built correctly"""
        habit_list_sh = ana.habit_creator(self.user_sh)
        completed_habits_sh = ana.find_completed_habits(habit_list_sh)
        comparison_data_sh = ana.analyse_all_habits(completed_habits_sh)
        assert list(comparison_data_sh.columns) == ["Brush teeth", "Dance", "Clean windows", "Clean bathroom",
                                                    "Go to dentist"]
        habit_list_rb = ana.habit_creator(self.user_rb)
        habits_with_data_rb = ana.find_completed_habits(habit_list_rb)
        comparison_data_rb = ana.analyse_all_habits(habits_with_data_rb)
        assert list(comparison_data_rb) == ["Brush teeth", "Dance"]

# File wurde durchgegangen, jede Funktion ist dokumentiert und alle wichtigen Funktionen wurden getestet