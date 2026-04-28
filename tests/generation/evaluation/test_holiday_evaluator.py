import pandas as pd
import pytest
from unittest.mock import patch

from ej.scheduler.generation.evaluation.holiday_evaluator import HolidayEvaluator
from ej.scheduler.generation.sampling_data_holder import SamplingRows

_EMPTY_HOLIDAYS = pd.DataFrame({
    "name": pd.Series([], dtype=str),
    "start": pd.Series([], dtype="datetime64[ns]"),
    "end": pd.Series([], dtype="datetime64[ns]"),
    "only_jf": pd.Series([], dtype=bool),
})


def make_evaluator():
    with patch("pandas.read_excel", return_value=_EMPTY_HOLIDAYS):
        ev = HolidayEvaluator("dummy.xlsx", 2025)
    return ev


def test_no_events_on_blocked_dates_returns_1(make_events):
    ev = make_evaluator()
    ev.blocked_dates = [50, 51, 52]
    arr = make_events(2, date=[1, 2])  # Not on blocked dates
    assert ev.evaluate(arr) == 1.0


def test_exact_formula_one_non_fixed_on_blocked_date(make_events):
    ev = make_evaluator()
    ev.blocked_dates = [10]
    arr = make_events(1, date=[10])  # FIXED=0 by default
    assert ev.evaluate(arr) == pytest.approx(0.8 ** 1)


def test_fixed_events_not_penalised(make_events):
    ev = make_evaluator()
    ev.blocked_dates = [10]
    arr = make_events(1, date=[10])
    arr[0, SamplingRows.FIXED.value] = 1
    assert ev.evaluate(arr) == 1.0


def test_comparison_fewer_hits_scores_higher(make_events):
    ev = make_evaluator()
    ev.blocked_dates = [10, 20]
    arr_a = make_events(2, date=[1, 2])   # 0 hits
    arr_b = make_events(2, date=[10, 20]) # 2 hits
    assert ev.evaluate(arr_a) > ev.evaluate(arr_b)


def test_edge_case_blocked_date_at_day_0(make_events):
    ev = make_evaluator()
    ev.blocked_dates = [0]
    arr = make_events(1, date=[0])
    assert ev.evaluate(arr) == pytest.approx(0.8 ** 1)


def test_edge_case_blocked_date_at_day_364(make_events):
    ev = make_evaluator()
    ev.blocked_dates = [364]
    arr = make_events(1, date=[364])
    assert ev.evaluate(arr) == pytest.approx(0.8 ** 1)
