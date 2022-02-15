from datetime import date, timedelta, datetime

import analyze as ana
import test_data
from user import UserDB


class TestHabitAnalysis(test_data.DataForTestingPytest):
    """This class tests the main functionalities provided by the application's analysis module (analyze.py)
    using the test data it inherits from the DataForTestingPytest class.

    Attributes: see the documentation of the DataForTestingPytest class
    """

    def test_create_data_frame(self):
        """test whether dataframes can be created from database tables"""
        habit_df = ana.create_data_frame(self.database, "Habit")
        assert len(habit_df) == 9
        user_df = ana.create_data_frame(self.database, "HabitAppUser")
        assert len(user_df) == 4
        completions_df = ana.create_data_frame(self.database, "Completions")
        assert len(completions_df) == 79

    def test_check_for_username(self):
        """test whether the database can be checked for the existance of usernames"""
        harry_p_existing = ana.check_for_username(self.harry_p)
        assert harry_p_existing is True
        harry_p = UserDB("HarryPotter", self.database)
        harry_potter_existing = ana.check_for_username(harry_p)
        assert harry_potter_existing is False

    def test_show_habit_data(self):
        """test whether a user's habit information is returned correctly"""
        defined_habits = ana.show_habit_data(self.harry_p)
        assert len(defined_habits) == 6
        assert "Conjuring" in defined_habits["Name"].to_list()

    def test_return_completions(self):
        """test if a habit's completion dates are returned correctly"""
        habit_completions_ginny_hp = ana.return_completions(self.ginny_hp)
        assert len(habit_completions_ginny_hp) == 20
        habit_completions_books_hg = ana.return_completions(self.books_hg)
        assert habit_completions_books_hg == ["2021-12-02", "2021-12-31"]

    def test_return_ordered_periodicities(self):
        """test whether the periodicities of a user's habits are correctly returned and in the correct order"""
        assert ana.return_ordered_periodicities(self.harry_p) == ["daily", "weekly", "monthly", "yearly"]
        assert ana.return_ordered_periodicities(self.hermione_g) == ["daily", "weekly"]
        assert ana.return_ordered_periodicities(self.ron_w) == []
        assert ana.return_ordered_periodicities(self.voldemort) == ["daily"]

    def test_return_habit_info(self):
        """test wehther habit information can be returned correctly for all habits and for habits with
        a certain periodicity"""
        all_habits = ana.return_habit_info(self.harry_p)
        assert len(all_habits) == 6
        weekly_habits = ana.return_habit_info(self.harry_p, "weekly")
        assert len(weekly_habits) == 2
        quaterly_habits = ana.return_habit_info(self.harry_p, "quarterly")
        assert len(quaterly_habits) == 0

    def test_calculate_period_starts(self):
        """tests if the period starts corresponding to the completion dates and the periodicity
        of a habit are calculated correctly"""
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
        final_periods_hedwig = ana.return_final_period_starts(self.hedwig_hp)
        final_periods_ginny = ana.return_final_period_starts(self.ginny_hp)
        final_periods_malfoy = ana.return_final_period_starts(self.malfoy_hp)
        final_periods_voldemort = ana.return_final_period_starts(self.kill_voldemort_hp)
        assert len(final_periods_hedwig) == 36
        assert len(final_periods_ginny) == 12
        assert len(final_periods_malfoy) == 9
        assert len(final_periods_voldemort) == 3

    def test_calculate_break_indices(self):
        """test if it is possible to calculate a habit's break indices correctly"""
        # test calculate_element_diffs function
        dates = [date(2021, 7, 3), date(2021, 7, 9), date(2021, 7, 10), date(2021, 8, 10)]
        assert ana.calculate_element_diffs(dates) == [timedelta(days=6), timedelta(days=1), timedelta(days=31)]

        # test calculate break_indices function
        final_periods_hedwig = ana.return_final_period_starts(self.hedwig_hp)
        final_periods_ginny = ana.return_final_period_starts(self.ginny_hp)
        final_periods_malfoy = ana.return_final_period_starts(self.malfoy_hp)
        final_periods_voldemort = ana.return_final_period_starts(self.kill_voldemort_hp)
        assert ana.calculate_break_indices(final_periods_hedwig, "daily") == [4, 25, 28, 29, 32, 34]
        assert ana.calculate_break_indices(final_periods_ginny, "weekly") == [4, 7, 10]
        assert ana.calculate_break_indices(final_periods_malfoy, "monthly") == [1, 7]
        assert ana.calculate_break_indices(final_periods_voldemort, "yearly") == [1]

    def test_calculate_longest_streak(self):
        """test if the a habit's longest streak is calculated correctly"""
        # test calculate_streak_lengths function
        assert ana.calculate_streak_lengths(self.hedwig_hp) == [5, 21, 3, 1, 3, 2]
        assert ana.calculate_streak_lengths(self.ginny_hp) == [5, 3, 3]
        assert ana.calculate_streak_lengths(self.malfoy_hp) == [2, 6]
        assert ana.calculate_streak_lengths(self.kill_voldemort_hp) == [2]

        # test calculate_longest_streak function
        assert ana.calculate_longest_streak(self.hedwig_hp) == 21
        assert ana.calculate_longest_streak(self.kill_voldemort_hp) == 2

    def test_calculate_longest_streak_of_all(self):
        """test if the longest streak of all habits of a user is calculated correctly"""
        # test habit_creator function
        habits_hp = ana.habit_creator(self.harry_p)
        assert len(habits_hp) == 6
        habits_hg = ana.habit_creator(self.hermione_g)
        assert len(habits_hg) == 2
        habits_rw = ana.habit_creator(self.ron_w)
        assert len(habits_rw) == 0

        # test find_completed_habits function
        habits_hp_data = ana.find_completed_habits(habits_hp)
        assert len(habits_hp_data) == 5
        habits_hg_data = ana.find_completed_habits(habits_hg)
        assert len(habits_hg_data) == 2
        habits_rw_data = ana.find_completed_habits(habits_rw)
        assert len(habits_rw_data) == 0

        # test calculate_longest_streak_per_habit function
        longest_streaks_hp = ana.calculate_longest_streak_per_habit(habits_hp_data)
        assert longest_streaks_hp["Meet Ginny"] == 5
        longest_streak_hg = ana.calculate_longest_streak_per_habit(habits_hg_data)
        assert longest_streak_hg["Read books"] == 1
        longest_streak_rw = ana.calculate_longest_streak_per_habit(habits_rw_data)
        assert longest_streak_rw is None

        # test calculate_longest_streak_of_all function
        longest_streak_all_hp = ana.calculate_longest_streak_of_all(habits_hp_data)
        assert longest_streak_all_hp == (21, ["Feed Hedwig"])
        longest_streak_all_hg = ana.calculate_longest_streak_of_all(habits_hg_data)
        assert longest_streak_all_hg == (1, ["Study", "Read books"])
        longest_streak_all_rw = ana.calculate_longest_streak_of_all(habits_rw_data)
        assert longest_streak_all_rw == (None, None)

    def test_completed_in_period(self):
        """test if it is possible to check if a habit was completed in the current or the previous period"""
        final_periods_hedwig_hp = ana.return_final_period_starts(self.hedwig_hp)
        final_periods_ginny_hp = ana.return_final_period_starts(self.ginny_hp)
        final_periods_study_hg = ana.return_final_period_starts(self.study_hg)
        assert ana.completed_in_period(final_periods_hedwig_hp, self.hedwig_hp.periodicity, "previous") is False
        assert ana.completed_in_period(final_periods_ginny_hp, self.ginny_hp.periodicity, "previous") is True
        assert ana.completed_in_period(final_periods_study_hg, self.study_hg.periodicity, "previous") is False
        assert ana.completed_in_period(final_periods_hedwig_hp, self.hedwig_hp.periodicity, "current") is False
        assert ana.completed_in_period(final_periods_ginny_hp, self.ginny_hp.periodicity, "current") is True
        assert ana.completed_in_period(final_periods_study_hg, self.study_hg.periodicity, "current") is True

    def test_calculate_curr_streak(self):
        """test if a habit's current streak is calculated correctly"""
        assert ana.calculate_curr_streak(self.hedwig_hp) == 0
        assert ana.calculate_curr_streak(self.ginny_hp) == 3
        assert ana.calculate_curr_streak(self.books_hg) == 0
        self.books_hg.check_off_habit(check_time=str(datetime.now()))
        assert ana.calculate_curr_streak(self.books_hg) == 1
        assert ana.calculate_curr_streak(self.malfoy_hp) == 6

    def test_calculate_completion_rate(self):
        """test if a habit's completion rate is calculated correctly (only daily & weekly habits)"""
        assert ana.calculate_completion_rate(self.hedwig_hp) == 6 / 28
        assert ana.calculate_completion_rate(self.ginny_hp) == 2 / 4
        self.ginny_hp.check_off_habit(str(datetime.now() - timedelta(weeks=3)))
        self.ginny_hp.check_off_habit(str(datetime.now() - timedelta(weeks=4)))
        assert ana.calculate_completion_rate(self.ginny_hp) == 4 / 4

    def test_calculate_break_no(self):
        """test if the number of breaks is calculated correctly"""
        assert ana.calculate_break_no(self.hedwig_hp) == 6
        assert ana.calculate_break_no(self.ginny_hp) == 2
        assert ana.calculate_break_no(self.malfoy_hp) == 1
        assert ana.calculate_break_no(self.kill_voldemort_hp) == 0
        self.conjure_hp.check_off_habit(str(datetime.now() - timedelta(days=1)))
        assert ana.calculate_break_no(self.conjure_hp) == 0

    def test_calculate_worst_completion_rate_of_all(self):
        """test if a user's lowest completion rate and the corresponding habit(s) are determined correctly"""
        # test if completions rates per habit are correctly calculated
        self.books_hg.check_off_habit(str(datetime.now() - timedelta(weeks=1)))
        self.study_hg.check_off_habit(str(datetime.now() - timedelta(weeks=1)))
        self.study_hg.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=1)))
        self.study_hg.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=2)))
        self.study_hg.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=3)))
        self.study_hg.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=4)))
        self.study_hg.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=5)))
        self.study_hg.check_off_habit(str(datetime.now() - timedelta(weeks=1, days=6)))

        completed_habits_hp = self.harry_p.completed_habits
        completed_habits_hg = self.hermione_g.completed_habits

        completion_rates_hp = ana.calculate_completion_rate_per_habit(completed_habits_hp)
        assert list(completion_rates_hp.values()) == [6 / 28, 2 / 4, 0 / 4]
        completion_rates_hg = ana.calculate_completion_rate_per_habit(completed_habits_hg)
        assert list(completion_rates_hg.values()) == [7 / 28, 1 / 4]

        # test if the lowest completion rate and the corresponding habit is identified correctly
        lowest_completion_rate_hp, worst_habit_hp = ana.calculate_worst_completion_rate_of_all(completed_habits_hp)
        assert round(lowest_completion_rate_hp) == 0
        assert worst_habit_hp == ["Train Quidditch"]
        lowest_completion_rate_hg, worst_habit_hg = ana.calculate_worst_completion_rate_of_all(completed_habits_hg)
        assert lowest_completion_rate_hg == 0.25
        assert worst_habit_hg == ["Study", "Read books"]

    def test_analyze_all_habits(self):
        """test if the dataframes to analyze all habits are built correctly"""
        habit_list_hp = ana.habit_creator(self.harry_p)
        completed_habits_hp = ana.find_completed_habits(habit_list_hp)
        comparison_data_hp = ana.analyze_all_habits(completed_habits_hp)
        assert list(comparison_data_hp.columns) == ["Feed Hedwig", "Meet Ginny", "Tease Malfoy", "Train Quidditch",
                                                    "Kill Voldemort"]
        habit_list_hg = ana.habit_creator(self.hermione_g)
        habits_with_data_hg = ana.find_completed_habits(habit_list_hg)
        comparison_data_hg = ana.analyze_all_habits(habits_with_data_hg)
        assert list(comparison_data_hg) == ["Study", "Read books"]
