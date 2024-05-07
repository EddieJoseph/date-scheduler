import multiprocessing

import numpy as np

from as_clean_evaluator import AsCleanEvaluator
from date_scheduler import iterate
from date_utils import get_week_days_of_year
from filtered_combined_sampler import FilteredCombinedSampler
from holiday_evaluator import HolidayEvaluator
from month_evaluator import MonthEvaluator
from no_change_date_sampler import NoChangeDateSampler
from normal_date_sampler import NormalDateSampler
from same_day_evaluator import SameDayEvaluator
from scheduler_config import SchedulerData, SchedulerConfig
from type_spread_evaluator import TypeSpreadEvaluator
from uniform_sampler import UniformSampler
from week_clumping_evaluator import WeekClumpingEvaluator
from weekend_evaluator import WeekendEvaluator


def worker(td):
    t_data = iterate(td[0], td[1], 1000)
    return t_data


def multithreaded_iteration(ti_data, ti_config, num_threads):
    queue = multiprocessing.Queue()

    td = [(ti_data, ti_config) for _ in range(num_threads)]
    with multiprocessing.Pool(processes=num_threads) as pool:
        results = pool.map(worker, td)
        best = results[0]
        for r in results:
            if r.score > best.score:
                best = r
        return best


if __name__ == '__main__':
    np.random.seed(74587)
    year = 2025
    get_week_days_of_year(year)

    no_change_sampler = NoChangeDateSampler()
    small_sampler = NormalDateSampler(variance=3)
    medium_sampler = NormalDateSampler(variance=30)
    large_sampler = NormalDateSampler(variance=150)

    # sampler = CombinedSampler([no_change_sampler,small_sampler,medium_sampler,large_sampler],[0.9,0.2,0.07,0.03])
    sampler = FilteredCombinedSampler([small_sampler, medium_sampler, large_sampler],
                                      [0.6, 0.35, 0.05], 2025, 'input/holidays.xlsx')
    initialization_sampler = UniformSampler()

    evaluator = TypeSpreadEvaluator()
    holiday_evaluator = HolidayEvaluator('input/holidays.xlsx')
    as_evaluator = AsCleanEvaluator(year)
    weekend_evaluator = WeekendEvaluator(year)
    week_clumping_evaluator = WeekClumpingEvaluator(year)
    same_day_evaluator = SameDayEvaluator()
    month_evaluator = MonthEvaluator()

    data = SchedulerData.create_from('input/ex_init.xlsx')
    config = SchedulerConfig.create_from('input/people.xlsx', year,
                                         [evaluator, holiday_evaluator, as_evaluator, weekend_evaluator,
                                          week_clumping_evaluator, same_day_evaluator, month_evaluator], sampler)

    for i in range(20):
        # data = iterate(data, config, 50)
        # print("Score: ", data.score)

        data = multithreaded_iteration(data, config, 32)
        print("Score: ", data.score)

    # for m in range(200):
    #     # res = scheduler.generate_candidate()
    #     # print(scheduler.evaluate_candidate(res))
    #     # print(res)
    #     # p = scheduler.iterate(1000)
    #     # print(p)
    #     # print(scheduler.get_result())
    #     for i in range(10):
    #         # res = scheduler.generate_candidate()
    #         # print(scheduler.evaluate_candidate(res))
    #         # print(res)
    #         p = scheduler.iterate(10000)
    #         # print(p)
    #         # print(scheduler.get_result())
    #
    #     # scheduler.iterate_until(100,0.02)
    #     print("max found: ", scheduler.get_max())
    #     # scheduler.save_dates('output/dates.xlsx')
    #     scheduler.save_max('output/dates_max' + str(m) + '.xlsx')
