import pytest

from ej.scheduler.generation.evaluation.assi_evaluator import AssiEvaluator
from ej.scheduler.generation.sampling_data_holder import SamplingRows


@pytest.fixture
def evaluator(make_sdh):
    # Use a real SamplingDataHolder so set_assi_types wires through map_types correctly.
    sdh = make_sdh(n=3, type=["ASI", "ASI", "ASI"], date=[10, 20, 30])
    ev = AssiEvaluator()
    ev.set_assi_types(sdh)
    return ev


def test_perfect_order_returns_1(make_events, evaluator):
    arr = make_events(3, date=[10, 20, 30])
    arr[:, SamplingRows.ORDER.value] = [1, 2, 3]
    assert evaluator.evaluate(arr) == 1.0


def test_exact_formula_one_violation(make_events, evaluator):
    # ORDER [1, 3, 2]: diff = [2, -1] → 1 descending → 0.5**1
    arr = make_events(3, date=[10, 20, 30])
    arr[:, SamplingRows.ORDER.value] = [1, 3, 2]
    assert evaluator.evaluate(arr) == pytest.approx(0.5 ** 1)


def test_exact_formula_two_violations(make_events, evaluator):
    # ORDER [3, 2, 1]: diff = [-1, -1] → 2 descending → 0.5**2
    arr = make_events(3, date=[10, 20, 30])
    arr[:, SamplingRows.ORDER.value] = [3, 2, 1]
    assert evaluator.evaluate(arr) == pytest.approx(0.5 ** 2)


def test_comparison_ordered_beats_reversed(make_events, evaluator):
    arr_a = make_events(4, date=[10, 20, 30, 40])
    arr_a[:, SamplingRows.ORDER.value] = [1, 2, 3, 4]

    arr_b = make_events(4, date=[10, 20, 30, 40])
    arr_b[:, SamplingRows.ORDER.value] = [4, 3, 2, 1]

    assert evaluator.evaluate(arr_a) > evaluator.evaluate(arr_b)


def test_order_minus_one_excluded(make_events, evaluator):
    # Middle event has ORDER=-1 (sentinel); excluded from diff computation.
    # Without exclusion: orders=[1,-1,2] → diffs=[-2,3] → 1 violation → 0.5
    # With exclusion: orders=[1,2] → diffs=[1] → 0 violations → 1.0
    arr = make_events(3, date=[10, 20, 30])
    arr[:, SamplingRows.ORDER.value] = [1, -1, 2]
    assert evaluator.evaluate(arr) == 1.0
