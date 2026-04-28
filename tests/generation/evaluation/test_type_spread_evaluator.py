import pytest

from ej.scheduler.generation.evaluation.type_spread_evaluator import TypeSpreadEvaluator


def _make_evaluator(make_sdh, n, types, dates, rb=None):
    kwargs = {"type": types, "date": dates}
    if rb is not None:
        kwargs["rb"] = rb
    sdh = make_sdh(n=n, **kwargs)
    ev = TypeSpreadEvaluator()
    ev.set_types(sdh)
    return ev, sdh.get_np_data()


def test_single_event_per_type_group_returns_1(make_sdh):
    # Only 1 event of type 'A' in RB group → generate_score_np returns 1 (< 2 events)
    ev, arr = _make_evaluator(make_sdh, 1, ["A"], [1], rb=[True])
    assert ev.evaluate(arr) == 1.0


def test_comparison_evenly_spaced_beats_clustered(make_sdh):
    # Dataset A: 4 RB events of type 'A' spread across the year
    ev_a, arr_a = _make_evaluator(
        make_sdh, 4, ["A"] * 4, [1, 91, 181, 271], rb=[True] * 4
    )
    # Dataset B: same type/group but all bunched together
    ev_b, arr_b = _make_evaluator(
        make_sdh, 4, ["A"] * 4, [1, 2, 3, 4], rb=[True] * 4
    )
    assert ev_a.evaluate(arr_a) > ev_b.evaluate(arr_b)


def test_comparison_more_events_evenly_spaced_still_beats_clustered(make_sdh):
    ev_a, arr_a = _make_evaluator(
        make_sdh, 4, ["A"] * 4, [30, 120, 210, 300], rb=[True] * 4
    )
    ev_b, arr_b = _make_evaluator(
        make_sdh, 4, ["A"] * 4, [10, 11, 12, 13], rb=[True] * 4
    )
    assert ev_a.evaluate(arr_a) > ev_b.evaluate(arr_b)


def test_excluded_types_do_not_affect_score(make_sdh):
    # 'ST' is in excluded_types → set_types produces empty self.types → score = 1.0
    ev, arr = _make_evaluator(make_sdh, 2, ["ST", "ST"], [1, 2], rb=[True, True])
    assert ev.evaluate(arr) == 1.0
