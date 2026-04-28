import pytest

from ej.scheduler.generation.evaluation.same_day_evaluator import SameDayEvaluator
from ej.scheduler.generation.sampling_data_holder import SamplingRows


@pytest.fixture
def evaluator(make_sdh):
    # Wire set_info_type through a real SamplingDataHolder so map_types is exercised.
    # In this SDH: type 'A' → ID 0, 'INFO' → ID 1.
    sdh = make_sdh(n=2, type=["A", "INFO"])
    ev = SameDayEvaluator()
    ev.set_info_type(sdh)
    return ev  # ev.info_type == 1


def test_perfect_score_all_non_info_unique_dates(make_events, evaluator):
    arr = make_events(3, date=[1, 2, 3])
    # TYPE defaults to 0 (non-INFO); all unique dates → no clashes
    assert evaluator.evaluate(arr) == 1.0


def test_info_events_sharing_date_not_penalised(make_events, evaluator):
    # Two INFO events (TYPE=1) on the same date; one non-INFO on a different date
    arr = make_events(3, date=[5, 5, 1])
    arr[:, SamplingRows.TYPE.value] = [1, 1, 0]  # INFO, INFO, A
    assert evaluator.evaluate(arr) == 1.0


def test_exact_formula_one_clash(make_events, evaluator):
    # Two non-INFO events share date 5 → 0.3**1
    arr = make_events(3, date=[5, 5, 1])
    # All TYPE=0 (non-INFO by default)
    assert evaluator.evaluate(arr) == pytest.approx(0.3 ** 1)


def test_exact_formula_two_clashes(make_events, evaluator):
    # Two pairs of non-INFO events share two different dates → 0.3**2
    arr = make_events(4, date=[5, 5, 10, 10])
    assert evaluator.evaluate(arr) == pytest.approx(0.3 ** 2)


def test_comparison_fewer_clashes_scores_higher(make_events, evaluator):
    arr_a = make_events(2, date=[1, 2])  # No clash
    arr_b = make_events(2, date=[5, 5])  # One clash
    assert evaluator.evaluate(arr_a) > evaluator.evaluate(arr_b)
