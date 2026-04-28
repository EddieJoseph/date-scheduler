import pandas as pd
import pytest
from unittest.mock import patch

from ej.scheduler.generation.evaluation.jf_holiday_evaluator import JfHolidayEvaluator
from ej.scheduler.generation.sampling_data_holder import SamplingRows

_EMPTY_HOLIDAYS = pd.DataFrame({
    "name": pd.Series([], dtype=str),
    "start": pd.Series([], dtype="datetime64[ns]"),
    "end": pd.Series([], dtype="datetime64[ns]"),
    "only_jf": pd.Series([], dtype=bool),
})

_JF_TYPE = 0   # TYPE column value used to represent JF events in make_events arrays
_NON_JF_TYPE = 1


def make_evaluator():
    with patch("pandas.read_excel", return_value=_EMPTY_HOLIDAYS):
        ev = JfHolidayEvaluator("dummy.xlsx", 2025)
    ev.jf_type = _JF_TYPE
    return ev


def test_no_jf_events_on_blocked_dates_returns_1(make_events):
    ev = make_evaluator()
    ev.blocked_dates = [50]
    arr = make_events(1, date=[99])  # TYPE=0 (JF) but not on blocked date
    assert ev.evaluate(arr) == 1.0


def test_non_jf_events_on_blocked_dates_not_penalised(make_events):
    ev = make_evaluator()
    ev.blocked_dates = [50]
    arr = make_events(1, date=[50])
    arr[0, SamplingRows.TYPE.value] = _NON_JF_TYPE  # Not JF
    assert ev.evaluate(arr) == 1.0


def test_exact_formula_one_jf_on_blocked_date(make_events):
    ev = make_evaluator()
    ev.blocked_dates = [50]
    arr = make_events(1, date=[50])
    arr[0, SamplingRows.TYPE.value] = _JF_TYPE  # JF event on blocked date
    assert ev.evaluate(arr) == pytest.approx(0.8 ** 1)


def test_comparison_fewer_jf_hits_scores_higher(make_events):
    ev = make_evaluator()
    ev.blocked_dates = [10, 20]

    arr_a = make_events(2, date=[1, 2])   # No JF events on blocked dates
    arr_a[:, SamplingRows.TYPE.value] = _JF_TYPE

    arr_b = make_events(2, date=[10, 20])  # 2 JF events on blocked dates
    arr_b[:, SamplingRows.TYPE.value] = _JF_TYPE

    assert ev.evaluate(arr_a) > ev.evaluate(arr_b)
