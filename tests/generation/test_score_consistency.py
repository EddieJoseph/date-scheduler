import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch

from ej.scheduler.generation.date_scheduler import generate_candidate, iterate, evaluate_candidate
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
from ej.scheduler.generation.sampling.filtered_combined_sampler import FilteredCombinedSampler
from ej.scheduler.generation.sampling.normal_date_sampler import NormalDateSampler
from ej.scheduler.generation.sampling_data_holder import SamplingDataHolder, SamplingRows
from ej.scheduler.util.row_names import RowNames
from ej.scheduler.util.scheduler_config import SchedulerConfig, SchedulerData

_EMPTY_HOLIDAYS = pd.DataFrame({
    "name": pd.Series([], dtype=str),
    "start": pd.Series([], dtype="datetime64[ns]"),
    "end": pd.Series([], dtype="datetime64[ns]"),
    "only_jf": pd.Series([], dtype=bool),
})


def _build_full_config(year: int):
    with patch("pandas.read_excel", return_value=_EMPTY_HOLIDAYS):
        small_sampler = NormalDateSampler(variance=3)
        medium_sampler = NormalDateSampler(variance=30)
        large_sampler = NormalDateSampler(variance=150)
        sampler = FilteredCombinedSampler([small_sampler, medium_sampler, large_sampler],
                                          [0.6, 0.3, 0.1], year, "dummy.xlsx")

        tse = TypeSpreadEvaluator()
        he = HolidayEvaluator("dummy.xlsx", year)
        jf = JfHolidayEvaluator("dummy.xlsx", year)
        ae = AsCleanEvaluator(year)
        we = WeekendEvaluator(year)
        wc = WeekClumpingEvaluator(year)
        sd = SameDayEvaluator()
        me = MonthEvaluator()
        assi = AssiEvaluator()
        wd = WeekDayEvaluator(year)

    evaluators = [tse, ae, he, we, sd, jf, wc, me, assi, wd]
    config = SchedulerConfig(year, evaluators, sampler)
    return config, (tse, jf, assi, sd, wd)


def _init_evaluators(data_np: SamplingDataHolder, evaluator_tuple):
    tse, jf, assi, sd, wd = evaluator_tuple
    tse.set_types(data_np)
    jf.set_jf_type(data_np)
    assi.set_assi_types(data_np)
    sd.set_info_type(data_np)
    wd.add_type("KP", data_np)
    wd.add_type("F", data_np)
    wd.add_type("ASI", data_np)


def test_generate_candidate_does_not_sort_rows(make_events):
    arr = make_events(3, date=[10, 20, 30])
    # Set dates such that index 0 gets date 50 (unsorted)
    arr[0, SamplingRows.DATE.value] = 50
    arr[1, SamplingRows.DATE.value] = 10
    arr[2, SamplingRows.DATE.value] = 20

    class DummySampler:
        def sample(self, dates):
            return dates.copy(), {0}

    config = SchedulerConfig(2025, [], DummySampler())
    candidate, changed_indices = generate_candidate(arr, config)

    # Verify rows remained at exact original indices
    assert candidate[0, SamplingRows.DATE.value] == 50
    assert candidate[1, SamplingRows.DATE.value] == 10
    assert candidate[2, SamplingRows.DATE.value] == 20
    assert changed_indices == {0}


def test_evaluators_invariant_to_row_order(make_events):
    # Test TypeSpreadEvaluator
    tse = TypeSpreadEvaluator()
    arr1 = make_events(3, date=[10, 50, 100], type=[1, 1, 1])
    arr2 = make_events(3, date=[50, 10, 100], type=[1, 1, 1])
    tse.precomputed_subsets = [np.array([0, 1, 2])]
    assert tse.evaluate(arr1) == pytest.approx(tse.evaluate(arr2))

    # Test AsCleanEvaluator
    ae = AsCleanEvaluator(2025)
    arr_as1 = make_events(3, date=[10, 50, 100], **{"as": [1, 1, 1]})
    arr_as2 = make_events(3, date=[100, 10, 50], **{"as": [1, 1, 1]})
    assert ae.evaluate(arr_as1) == pytest.approx(ae.evaluate(arr_as2))

    # Test AssiEvaluator
    assi = AssiEvaluator()
    assi.assi_types = np.array([1])
    arr_assi1 = make_events(3, date=[10, 50, 100], type=[1, 1, 1], order=[1, 2, 3])
    arr_assi2 = make_events(3, date=[100, 10, 50], type=[1, 1, 1], order=[3, 1, 2])
    assert assi.evaluate(arr_assi1) == pytest.approx(assi.evaluate(arr_assi2))


def test_score_consistency_after_iterate_and_reload(make_scheduler_data):
    year = 2026
    np.random.seed(42)

    data = make_scheduler_data(30)
    data_np = SamplingDataHolder(data)

    config1, eval_tuple1 = _build_full_config(year)
    _init_evaluators(data_np, eval_tuple1)

    # Run optimization iterations
    data_np = iterate(data_np, config1, iterations=200, limit=False)
    opt_score = data_np.get_score()

    # Direct evaluation of the optimized numpy array
    direct_score = evaluate_candidate(data_np.get_np_data(), config1)
    assert opt_score == pytest.approx(direct_score, rel=1e-9)

    # Save to SchedulerData and reload into a fresh SamplingDataHolder
    saved_sd = data_np.get_scheduler_data()
    reloaded_data_np = SamplingDataHolder(saved_sd)

    config2, eval_tuple2 = _build_full_config(year)
    _init_evaluators(reloaded_data_np, eval_tuple2)

    reloaded_score = evaluate_candidate(reloaded_data_np.get_np_data(), config2)

    # Both scores MUST match exactly
    assert opt_score == pytest.approx(reloaded_score, rel=1e-9)
