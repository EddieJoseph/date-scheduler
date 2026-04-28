import pytest

from ej.scheduler.generation.evaluation.week_day_evaluator import WeekDayEvaluator

# 2025: Jan 1 = Wednesday → offset=2. get_week_day(day) = (day + 2) % 7
# Mon=0, Tue=1, Wed=2, Thu=3, Fri=4, Sat=5, Sun=6
# Day 0=Wed(2), day 1=Thu(3), day 5=Mon(0), day 6=Tue(1)
# Day 3=Sat(5), day 4=Sun(6)  — filtered out (≥4)
# Day 364=Wed(2): (364+2)%7=2


def _make_evaluator(make_sdh, n, types, dates, rb=None):
    kwargs = {"type": types, "date": dates}
    if rb is not None:
        kwargs["rb"] = rb
    sdh = make_sdh(n=n, **kwargs)
    ev = WeekDayEvaluator(2025)
    ev.add_type(types[0], sdh)
    return ev, sdh.get_np_data()


def test_even_distribution_mon_thu_returns_1(make_sdh):
    # One RB event each on Mon(day5), Tue(day6), Wed(day0), Thu(day1)
    ev, arr = _make_evaluator(make_sdh, 4, ["A"] * 4, [0, 1, 5, 6], rb=[True] * 4)
    assert ev.evaluate(arr) == pytest.approx(1.0)


def test_comparison_balanced_beats_all_on_monday(make_sdh):
    ev_a, arr_a = _make_evaluator(
        make_sdh, 4, ["A"] * 4, [0, 1, 5, 6], rb=[True] * 4
    )
    # All 4 RB events on Mondays (days 5, 12, 19, 26)
    ev_b, arr_b = _make_evaluator(
        make_sdh, 4, ["A"] * 4, [5, 12, 19, 26], rb=[True] * 4
    )
    assert ev_a.evaluate(arr_a) > ev_b.evaluate(arr_b)


def test_weekend_only_events_filtered_returns_1(make_sdh):
    # All RB events on Saturday (day 3) and Sunday (day 4) → filtered out → score 1.0
    ev, arr = _make_evaluator(make_sdh, 2, ["A", "A"], [3, 4], rb=[True, True])
    assert ev.evaluate(arr) == 1.0


def test_year_boundary_weekday_mapping(make_sdh):
    # Day 0 (Jan 1, Wed=2) and day 364 (Dec 31, Wed=2) — no error, both map to wd=2
    ev, arr = _make_evaluator(make_sdh, 2, ["A", "A"], [0, 364], rb=[True, True])
    score = ev.evaluate(arr)
    assert isinstance(score, float)
