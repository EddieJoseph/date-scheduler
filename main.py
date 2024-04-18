# This is a sample Python script.
import datetime

import numpy as np
import pandas as pd

from as_clean_evaluator import AsCleanEvaluator
from combined_sampler import CombinedSampler
from date_scheduler import DateScheduler
from date_utils import convert_to_day_of_year, get_week_days_of_year
from filtered_combined_sampler import FilteredCombinedSampler
from group_utils import get_company
from holiday_evaluator import HolidayEvaluator
from no_change_date_sampler import NoChangeDateSampler
from normal_date_sampler import NormalDateSampler
from same_day_evaluator import SameDayEvaluator
from type_spread_evaluator import TypeSpreadEvaluator
from uniform_sampler import UniformSampler
from week_clumping_evaluator import WeekClumpingEvaluator
from weekend_evaluator import WeekendEvaluator

# Press the green button in the gutter to run the script.


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
                                      [ 0.6, 0.35, 0.05], 2025, 'input/holidays.xlsx')
    initialization_sampler = UniformSampler()

    evaluator = TypeSpreadEvaluator()
    holiday_evaluator = HolidayEvaluator('input/holidays.xlsx')
    as_evaluator = AsCleanEvaluator(year)
    weekend_evaluator = WeekendEvaluator(year)
    week_clumping_evaluator = WeekClumpingEvaluator(year)
    same_day_evaluator = SameDayEvaluator()

    scheduler = DateScheduler(year)
    scheduler.load_dates('input/dates_imp3.xlsx')
    scheduler.load_people('input/people.xlsx')

    scheduler.set_sampler(sampler)
    scheduler.add_evaluator(evaluator)
    scheduler.add_evaluator(holiday_evaluator)
    scheduler.add_evaluator(as_evaluator)
    scheduler.add_evaluator(weekend_evaluator)
    scheduler.add_evaluator(week_clumping_evaluator)
    scheduler.add_evaluator(same_day_evaluator)
    for m in range(200):
        # res = scheduler.generate_candidate()
        # print(scheduler.evaluate_candidate(res))
        # print(res)
        # p = scheduler.iterate(1000)
        # print(p)
        # print(scheduler.get_result())
        for i in range(10):
            # res = scheduler.generate_candidate()
            # print(scheduler.evaluate_candidate(res))
            # print(res)
            p = scheduler.iterate(1000)
            # print(p)
            # print(scheduler.get_result())

        # scheduler.iterate_until(100,0.02)
        print("max found: ", scheduler.get_max())
        # scheduler.save_dates('output/dates.xlsx')
        scheduler.save_max('output/dates_max' + str(m) + '.xlsx')
