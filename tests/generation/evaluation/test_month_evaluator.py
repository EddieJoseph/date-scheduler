import pytest

from ej.scheduler.generation.evaluation.month_evaluator import MonthEvaluator
from ej.scheduler.generation.sampling_data_holder import SamplingRows
from ej.scheduler.util.date_utils import get_month_from_day_of_year

# Days are 0-indexed: day 0–30 = month 1, day 31–58 = month 2, etc.
# MONTH=-1 means no constraint (ignored).


@pytest.fixture
def evaluator():
    return MonthEvaluator()


def test_perfect_score_event_in_correct_month(make_events, evaluator):
    # MONTH=1, DATE=0 (Jan 1 = month 1)
    arr = make_events(1, date=[0], month=[1])
    assert evaluator.evaluate(arr) == 1.0


def test_month_minus_one_ignored(make_events, evaluator):
    # MONTH=-1 event at DATE=31 (month 2) is not penalised; MONTH=1 at DATE=0 is correct.
    # If the -1 event were counted it would add a violation, so score would drop below 1.0.
    arr = make_events(2, date=[0, 31], month=[1, -1])
    assert evaluator.evaluate(arr) == 1.0


def test_exact_formula_one_month_off(make_events, evaluator):
    # MONTH=1 but DATE=31 (Feb 1 = month 2) → diff=|1-2|=1
    arr = make_events(1, date=[31], month=[1])
    assert evaluator.evaluate(arr) == pytest.approx(0.85 ** 1)


def test_comparison_closer_beats_further(make_events, evaluator):
    # 1 month off vs 2 months off
    arr_a = make_events(1, date=[31], month=[1])   # 1 month off
    arr_b = make_events(1, date=[59], month=[1])   # 2 months off
    assert evaluator.evaluate(arr_a) > evaluator.evaluate(arr_b)


def test_edge_case_last_day_of_january(make_events, evaluator):
    # Day 30 = Jan 31 → month 1; MONTH=1 → no violation
    assert get_month_from_day_of_year(30) == 1
    arr = make_events(1, date=[30], month=[1])
    assert evaluator.evaluate(arr) == 1.0


def test_edge_case_first_day_of_february(make_events, evaluator):
    # Day 31 = Feb 1 → month 2; MONTH=1 → 1 violation
    assert get_month_from_day_of_year(31) == 2
    arr = make_events(1, date=[31], month=[1])
    assert evaluator.evaluate(arr) == pytest.approx(0.85 ** 1)
