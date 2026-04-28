import pytest

from ej.scheduler.generation.evaluation.week_clumping_evaluator import WeekClumpingEvaluator

# 2025: Jan 1 = Wednesday → wd_offset=2.
# get_week(day) = floor((day + 2) / 7)
# Week 0: days 0–4, week 1: days 5–11, ...
# Last Mon-Sun week (week 52): days 362–364 (Dec 29–31).


@pytest.fixture
def evaluator():
    return WeekClumpingEvaluator(2025)


def test_at_most_two_per_week_returns_1(make_events, evaluator):
    # 4 events in 4 different weeks
    arr = make_events(4, date=[0, 7, 14, 21])
    assert evaluator.evaluate(arr) == 1.0


def test_exact_formula_three_per_week(make_events, evaluator):
    # Days 0, 1, 2 → all in week 0 → count=3 > 2
    arr = make_events(3, date=[0, 1, 2])
    assert evaluator.evaluate(arr) == pytest.approx(0.99 ** 1)


def test_exact_formula_four_per_week(make_events, evaluator):
    # Days 0, 1, 2, 3 → all in week 0 → count=4 > 3
    arr = make_events(4, date=[0, 1, 2, 3])
    assert evaluator.evaluate(arr) == pytest.approx(0.99 ** 1 * 0.9 ** 1)


def test_comparison_spread_beats_clustered(make_events, evaluator):
    # Spread: one event per week for 6 weeks
    arr_a = make_events(6, date=[0, 7, 14, 21, 28, 35])
    # Clustered: 6 events in the same week
    arr_b = make_events(6, date=[0, 1, 2, 3, 4, 5])
    assert evaluator.evaluate(arr_a) > evaluator.evaluate(arr_b)


def test_last_week_of_2025_edge_case(make_events, evaluator):
    # Days 362, 363, 364 = Dec 29, 30, 31 → all in week 52 → score < 1.0
    arr = make_events(3, date=[362, 363, 364])
    score = evaluator.evaluate(arr)
    assert score < 1.0
