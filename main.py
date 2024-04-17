# This is a sample Python script.
import datetime

import numpy as np

from combined_sampler import CombinedSampler
from date_scheduler import DateScheduler
from group_utils import get_company
from no_change_date_sampler import NoChangeDateSampler
from normal_date_sampler import NormalDateSampler
from type_spread_evaluator import TypeSpreadEvaluator
from uniform_sampler import UniformSampler


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    np.random.seed(0)
    min_date = datetime.date(2025, 1, 1)
    max_date = datetime.date(2025, 12, 31)

    no_change_sampler = NoChangeDateSampler()
    small_sampler = NormalDateSampler(variance=3, min=min_date, max=max_date)
    medium_sampler = NormalDateSampler(variance=30, min=min_date, max=max_date)
    large_sampler = NormalDateSampler(variance=150, min=min_date, max=max_date)

    sampler = CombinedSampler([no_change_sampler,small_sampler,medium_sampler,large_sampler],[0.7,0.08,0.2,0.02])


    # sampler = NormalDateSampler(variance=30, min=min_date, max=max_date)
    initialization_sampler = UniformSampler(min=min_date, max=max_date)

    evaluator = TypeSpreadEvaluator(min_date, max_date)


    scheduler = DateScheduler()
    scheduler.load_dates('input/dates.xlsx')
    scheduler.load_people('input/people.xlsx')

    rb = get_company(scheduler.get_groups(), 'RB')



    scheduler.initialize(initialization_sampler)
    scheduler.set_sampler(sampler)
    scheduler.add_evaluator(evaluator)
    # for i in range(200):
    #     # res = scheduler.generate_candidate()
    #     # print(scheduler.evaluate_candidate(res))
    #     # print(res)
    #     p = scheduler.iterate(100)
    #     # print(p)
    #     # print(scheduler.get_result())

    scheduler.iterate_until(100,0.7)
    scheduler.save_dates('output/dates.xlsx')


