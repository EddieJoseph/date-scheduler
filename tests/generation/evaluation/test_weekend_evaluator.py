import pytest

from ej.scheduler.generation.evaluation.weekend_evaluator import WeekendEvaluator
from ej.scheduler.generation.sampling_data_holder import SamplingRows

# 2025: Jan 1 = Wednesday. Days are 0-indexed.
# Day 0 = Jan 1 (Wed), day 2 = Jan 3 (Fri), day 3 = Jan 4 (Sat).
# Day 360 = Dec 27 (Sat) — last Saturday of 2025.


@pytest.fixture
def evaluator():
    return WeekendEvaluator(2025)


def test_perfect_score_sat_on_saturday_others_on_weekday(make_events, evaluator):
    # SAT=1 event on day 3 (Saturday), SAT=0 event on day 0 (Wednesday)
    arr = make_events(2, date=[0, 3])
    arr[1, SamplingRows.SAT.value] = 1
    assert evaluator.evaluate(arr) == 1.0


def test_exact_formula_non_sat_on_friday(make_events, evaluator):
    # Day 2 = Jan 3, 2025 = Friday; SAT=0 → counts as non-SAT on weekend
    arr = make_events(1, date=[2])
    assert evaluator.evaluate(arr) == pytest.approx(0.6 ** 1)


def test_exact_formula_sat_not_on_saturday(make_events, evaluator):
    # SAT=1 event on day 0 (Wednesday) → penalty
    arr = make_events(1, date=[0])
    arr[0, SamplingRows.SAT.value] = 1
    assert evaluator.evaluate(arr) == pytest.approx(0.6 ** 1)


def test_fixed_events_not_penalised(make_events, evaluator):
    # Fixed non-SAT event on Friday → not counted
    arr = make_events(1, date=[2])
    arr[0, SamplingRows.FIXED.value] = 1
    assert evaluator.evaluate(arr) == 1.0


def test_comparison_compliant_beats_violating(make_events, evaluator):
    # Dataset A: all events on correct day types
    arr_a = make_events(1, date=[0])  # SAT=0 on Wednesday → OK

    # Dataset B: 3 violations (non-SAT events on Friday)
    arr_b = make_events(3, date=[2, 9, 16])  # Fridays
    assert evaluator.evaluate(arr_a) > evaluator.evaluate(arr_b)


def test_edge_case_last_saturday_of_2025(make_events, evaluator):
    # Day 360 = Dec 27, 2025 = Saturday → SAT=1 event recognised, no penalty
    arr = make_events(1, date=[360])
    arr[0, SamplingRows.SAT.value] = 1
    assert evaluator.evaluate(arr) == 1.0
