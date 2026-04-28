import time

import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch

from ej.scheduler.generation.evaluation.as_clean_evaluator import AsCleanEvaluator
from ej.scheduler.generation.evaluation.assi_evaluator import AssiEvaluator
from ej.scheduler.generation.evaluation.holiday_evaluator import HolidayEvaluator
from ej.scheduler.generation.evaluation.jf_holiday_evaluator import JfHolidayEvaluator
from ej.scheduler.generation.evaluation.month_evaluator import MonthEvaluator
from ej.scheduler.generation.evaluation.same_day_evaluator import SameDayEvaluator
from ej.scheduler.generation.evaluation.type_spread_evaluator import TypeSpreadEvaluator
from ej.scheduler.generation.evaluation.week_clumping_evaluator import WeekClumpingEvaluator
from ej.scheduler.generation.evaluation.week_day_evaluator import WeekDayEvaluator
from ej.scheduler.generation.evaluation.weekend_evaluator import WeekendEvaluator
from ej.scheduler.generation.sampling_data_holder import SamplingDataHolder
from ej.scheduler.util.row_names import RowNames
from ej.scheduler.util.scheduler_config import SchedulerData

_EMPTY_HOLIDAYS = pd.DataFrame({
    "name": pd.Series([], dtype=str),
    "start": pd.Series([], dtype="datetime64[ns]"),
    "end": pd.Series([], dtype="datetime64[ns]"),
    "only_jf": pd.Series([], dtype=bool),
})

ITERATIONS = 5000
YEAR = 2025


def _build_fixture():
    """Build a realistic 70-event candidate array with representative type/group distribution."""
    n = 70
    # Types: 12 KP, 12 F, 6 ASI, 4 ASIKVK, 14 J, 5 INFO, 17 UEB
    types = (["KP"] * 12 + ["F"] * 12 + ["ASI"] * 6 + ["ASIKVK"] * 4
             + ["J"] * 14 + ["INFO"] * 5 + ["UEB"] * 17)

    dates = list(np.linspace(5, 360, n).astype(int))

    rb = [False] * n
    kb = [False] * n
    gb = [False] * n
    for i in range(0, 4): rb[i] = True    # KP RB
    for i in range(4, 8): kb[i] = True    # KP KB
    for i in range(8, 12): gb[i] = True   # KP GB
    for i in range(12, 16): rb[i] = True  # F RB
    for i in range(16, 20): kb[i] = True  # F KB
    for i in range(20, 24): gb[i] = True  # F GB
    for i in range(61, 65): rb[i] = True  # UEB RB
    for i in range(65, 69): kb[i] = True  # UEB KB

    as_col = [False] * n
    for i in range(53, 61): as_col[i] = True  # UEB with AS flag

    month = [np.nan] * n
    for i in range(34, 39): month[i] = 3.0   # J events targeting March
    for i in range(39, 44): month[i] = 9.0   # J events targeting September

    order = [np.nan] * n
    for i in range(24, 30): order[i] = float(i - 24)  # ASI events in order
    for i in range(30, 34): order[i] = float(i - 30)  # ASIKVK events in order

    df = pd.DataFrame({
        RowNames.DATE.value: dates,
        RowNames.NAME.value: [f"event-{i}" for i in range(n)],
        RowNames.TYPE.value: types,
        RowNames.AS.value: as_col,
        RowNames.RB.value: rb,
        RowNames.KB.value: kb,
        RowNames.GB.value: gb,
        RowNames.MOT.value: [False] * n,
        RowNames.ASI.value: [False] * n,
        RowNames.KADER.value: [False] * n,
        RowNames.OFF.value: [False] * n,
        RowNames.SAT.value: [False] * n,
        RowNames.MONTH.value: month,
        RowNames.FIXED.value: [False] * n,
        RowNames.ORDER.value: order,
        RowNames.TIME.value: [""] * n,
        RowNames.THEME.value: [""] * n,
        RowNames.CALLED_UP.value: [""] * n,
        RowNames.RESPONSIBLE.value: [""] * n,
        RowNames.DETAILS.value: [""] * n,
        RowNames.INCLUDE.value: [True] * n,
        RowNames.ID.value: [f"event-{i}" for i in range(n)],
    }).reset_index(drop=True)
    df[RowNames.DATE.value] = df[RowNames.DATE.value].astype(np.int64)

    sdh = SamplingDataHolder(SchedulerData(df, 0.0))
    return sdh, sdh.get_np_data()


def _build_evaluators(sdh):
    with patch("pandas.read_excel", return_value=_EMPTY_HOLIDAYS):
        holiday_evaluator = HolidayEvaluator("dummy.xlsx", YEAR)
        jf_holiday_evaluator = JfHolidayEvaluator("dummy.xlsx", YEAR)

    type_spread_evaluator = TypeSpreadEvaluator()
    type_spread_evaluator.set_types(sdh)

    jf_holiday_evaluator.set_jf_type(sdh)

    assi_evaluator = AssiEvaluator()
    assi_evaluator.set_assi_types(sdh)

    same_day_evaluator = SameDayEvaluator()
    same_day_evaluator.set_info_type(sdh)

    week_day_evaluator = WeekDayEvaluator(YEAR)
    week_day_evaluator.add_type("KP", sdh)
    week_day_evaluator.add_type("F", sdh)
    week_day_evaluator.add_type("ASI", sdh)

    return [
        type_spread_evaluator,
        AsCleanEvaluator(YEAR),
        holiday_evaluator,
        WeekendEvaluator(YEAR),
        same_day_evaluator,
        jf_holiday_evaluator,
        WeekClumpingEvaluator(YEAR),
        MonthEvaluator(),
        assi_evaluator,
        week_day_evaluator,
    ]


def test_evaluator_performance(capsys):
    """Time each evaluator over ITERATIONS calls. No timing assertions — run with -s to see output."""
    sdh, candidate = _build_fixture()
    evaluators = _build_evaluators(sdh)

    timings = {}
    for evaluator in evaluators:
        start = time.perf_counter()
        for _ in range(ITERATIONS):
            evaluator.evaluate(candidate)
        timings[evaluator.get_name()] = time.perf_counter() - start

    total_individual = sum(timings.values())

    start = time.perf_counter()
    for _ in range(ITERATIONS):
        score = 1.0
        for evaluator in evaluators:
            score *= evaluator.evaluate(candidate)
    total_composite = time.perf_counter() - start

    with capsys.disabled():
        print(f"\n--- Evaluator Performance ({ITERATIONS} iterations, year={YEAR}) ---")
        for name, t in timings.items():
            print(f"  {name:<30s}  {t * 1000:8.1f} ms  ({100 * t / total_individual:5.1f}%)")
        print(f"  {'--- sum of individuals':<30s}  {total_individual * 1000:8.1f} ms")
        print(f"  {'Total composite loop':<30s}  {total_composite * 1000:8.1f} ms")

    # Incremental evaluation benchmark: simulate 1 changed row per step
    from ej.scheduler.generation.evaluation.type_spread_evaluator import TypeSpreadEvaluator
    from ej.scheduler.generation.evaluation.week_day_evaluator import WeekDayEvaluator

    type_spread_ev = next(e for e in evaluators if isinstance(e, TypeSpreadEvaluator))
    week_day_ev = next(e for e in evaluators if isinstance(e, WeekDayEvaluator))

    changed = {5}  # one changed row
    cache_ts: dict = {}
    cache_wd: dict = {}

    start = time.perf_counter()
    for _ in range(ITERATIONS):
        _, cache_ts = type_spread_ev.evaluate_incremental(candidate, changed, cache_ts)
    t_ts_inc = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(ITERATIONS):
        _, cache_wd = week_day_ev.evaluate_incremental(candidate, changed, cache_wd)
    t_wd_inc = time.perf_counter() - start

    with capsys.disabled():
        print(f"\n--- Incremental Evaluation ({ITERATIONS} iterations, 1 changed row) ---")
        print(f"  {'TypeSpreadEvaluator full':<35s}  {timings['TypeSpreadEvaluator'] * 1000:8.1f} ms")
        print(f"  {'TypeSpreadEvaluator incremental':<35s}  {t_ts_inc * 1000:8.1f} ms  ({timings['TypeSpreadEvaluator'] / t_ts_inc:.1f}x speedup)")
        print(f"  {'WeekDayEvaluator full':<35s}  {timings['WeekDayEvaluator'] * 1000:8.1f} ms")
        print(f"  {'WeekDayEvaluator incremental':<35s}  {t_wd_inc * 1000:8.1f} ms  ({timings['WeekDayEvaluator'] / t_wd_inc:.1f}x speedup)")
