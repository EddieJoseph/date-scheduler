# This is a sample Python script.
import datetime

import numpy as np
import pandas as pd

from combined_sampler import CombinedSampler
from date_scheduler import DateScheduler
from date_utils import convert_to_day_of_year
from group_utils import get_company
from no_change_date_sampler import NoChangeDateSampler
from normal_date_sampler import NormalDateSampler
from type_spread_evaluator import TypeSpreadEvaluator
from uniform_sampler import UniformSampler


# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    np.random.seed(74587)
    year = 2025

    no_change_sampler = NoChangeDateSampler()
    small_sampler = NormalDateSampler(variance=3)
    medium_sampler = NormalDateSampler(variance=30)
    large_sampler = NormalDateSampler(variance=150)

    sampler = CombinedSampler([no_change_sampler,small_sampler,medium_sampler,large_sampler],[0.9,0.2,0.07,0.03])
    initialization_sampler = UniformSampler()

    evaluator = TypeSpreadEvaluator()


    scheduler = DateScheduler(year)
    scheduler.load_dates('input/dates.xlsx')
    scheduler.load_people('input/people.xlsx')


    scheduler.set_sampler(sampler)
    scheduler.add_evaluator(evaluator)
    for m in range(20):
        # res = scheduler.generate_candidate()
        # print(scheduler.evaluate_candidate(res))
        # print(res)
        p = scheduler.iterate(1000)
        # print(p)
        # print(scheduler.get_result())
        # for i in range(200):
        #     # res = scheduler.generate_candidate()
        #     # print(scheduler.evaluate_candidate(res))
        #     # print(res)
        #     p = scheduler.iterate(100)
            # print(p)
            # print(scheduler.get_result())

        # scheduler.iterate_until(100,0.02)
        print("max found: ", scheduler.get_max())
        # scheduler.save_dates('output/dates.xlsx')
        scheduler.save_max('output/dates_max'+str(m)+'.xlsx')


