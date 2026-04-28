import pytest

from ej.scheduler.generation.evaluation.as_clean_evaluator import AsCleanEvaluator
from ej.scheduler.generation.sampling_data_holder import SamplingRows

# 2025: Jan 1 = Wednesday (weekday 2). Days are 0-indexed.
# compare(d1, d2) counts weekdays in the half-open interval [d1, d2).


@pytest.fixture
def evaluator():
    return AsCleanEvaluator(2025)


def test_no_as_events_returns_1(make_events, evaluator):
    arr = make_events(2)  # AS column defaults to 0
    assert evaluator.evaluate(arr) == 1.0


def test_well_separated_returns_1(make_events, evaluator):
    # Days 0 and 5: compare(0,5) = weekdays in {0,1,2,3,4} = Wed,Thu,Fri = 3 >= min_days=3
    arr = make_events(2, date=[0, 5])
    arr[:, SamplingRows.AS.value] = 1
    assert evaluator.evaluate(arr) == 1.0


def test_exact_formula_one_pair_below_threshold(make_events, evaluator):
    # Days 0 and 2: compare(0,2) = weekdays in {0,1} = Wed,Thu = 2 < 3 → penalty
    arr = make_events(2, date=[0, 2])
    arr[:, SamplingRows.AS.value] = 1
    assert evaluator.evaluate(arr) == pytest.approx(0.6 ** 1)


def test_comparison_well_separated_beats_clustered(make_events, evaluator):
    arr_a = make_events(2, date=[0, 10])
    arr_a[:, SamplingRows.AS.value] = 1

    arr_b = make_events(2, date=[0, 1])
    arr_b[:, SamplingRows.AS.value] = 1

    assert evaluator.evaluate(arr_a) > evaluator.evaluate(arr_b)


def test_year_end_edge_case(make_events, evaluator):
    # Days 360 (Dec 27, Sat) and 364 (Dec 31, Wed): compare(360,364) = 2 weekdays
    arr = make_events(2, date=[360, 364])
    arr[:, SamplingRows.AS.value] = 1
    score = evaluator.evaluate(arr)
    assert 0 < score < 1
