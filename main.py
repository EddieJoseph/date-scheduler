import multiprocessing

import numpy as np

from as_clean_evaluator import AsCleanEvaluator
from combined_sampler import CombinedSampler
from convert_output import convert_process_result, convert_output
from date_scheduler import iterate, print_details
from date_utils import get_week_days_of_year
from filtered_combined_sampler import FilteredCombinedSampler
from holiday_evaluator import HolidayEvaluator
from jf_holiday_evaluator import JfHolidayEvaluator
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
    t_data = iterate(td[0], td[1], td[2], td[3])
    return t_data


def multithreaded_iteration(ti_data:SchedulerData, ti_config, num_threads, num_iterations=1, limit=False):
    queue = multiprocessing.Queue()

    td = [(ti_data, ti_config, num_iterations, limit) for _ in range(num_threads)]
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
    jf_holiday_evaluator = JfHolidayEvaluator('input/holidays.xlsx')
    as_evaluator = AsCleanEvaluator(year)
    weekend_evaluator = WeekendEvaluator(year)
    week_clumping_evaluator = WeekClumpingEvaluator(year)
    same_day_evaluator = SameDayEvaluator()
    month_evaluator = MonthEvaluator()

    # data = SchedulerData.create_from('input/best_input.xlsx')
    data = SchedulerData.create_from('input/dates_reduced.xlsx')
    config = SchedulerConfig.create_from('input/people.xlsx', year,
                                         [evaluator, holiday_evaluator, as_evaluator, weekend_evaluator,
                                          week_clumping_evaluator, same_day_evaluator, month_evaluator, jf_holiday_evaluator], sampler)

    for i in range(1000):
        # data = iterate(data, config, 20, True)
        data = multithreaded_iteration(data, config, 32, 1000, True)
        # print("Score: ", data.score)
        # print_details(data, config)
        print_details(data, config)


        data.save_to(year, 'output/dates' + str(i) + '.xlsx')
        convert_output('output/dates' + str(i) + '.xlsx','output/dates_pretty' + str(i) + '.xlsx')

    # for i in range(20, 40):
    #     # data = iterate(data, config, 1000, True)
    #     # print("Score: ", data.score)
    #
    #
    #     data = multithreaded_iteration(data, config, 32, 2000, True)
    #     print("Score: ", data.score)
    #
    #     data.save_to(year, 'output/dates' + str(i) + '.xlsx')
    #     convert_output('output/dates' + str(i) + '.xlsx','output/dates_pretty' + str(i) + '.xlsx')
    #
    # for i in range(40, 45):
    #     data = multithreaded_iteration(data, config, 32, 2000, False)
    #     print("Score: ", data.score)
    #     data.save_to(year, 'output/dates' + str(i) + '.xlsx')
    #     convert_output('output/dates' + str(i) + '.xlsx','output/dates_pretty' + str(i) + '.xlsx')
    # for i in range(45, 60):
    #     data = multithreaded_iteration(data, config, 32, 2000, False)
    #     print("Score: ", data.score)
    #     data.save_to(year, 'output/dates' + str(i) + '.xlsx')
    #     convert_output('output/dates' + str(i) + '.xlsx','output/dates_pretty' + str(i) + '.xlsx')
    #
    # for i in range(60, 65):
    #     data = multithreaded_iteration(data, config, 32, 2000, False)
    #     print("Score: ", data.score)
    #     data.save_to(year, 'output/dates' + str(i) + '.xlsx')
    #     convert_output('output/dates' + str(i) + '.xlsx','output/dates_pretty' + str(i) + '.xlsx')
    # for i in range(65, 80):
    #     data = multithreaded_iteration(data, config, 32, 2000, False)
    #     print("Score: ", data.score)
    #     data.save_to(year, 'output/dates' + str(i) + '.xlsx')
    #     convert_output('output/dates' + str(i) + '.xlsx','output/dates_pretty' + str(i) + '.xlsx')
    #
    # for i in range(80, 120):
    #     data = multithreaded_iteration(data, config, 32, 4000, True)
    #     print("Score: ", data.score)
    #     data.save_to(year, 'output/dates' + str(i) + '.xlsx')
    #     convert_output('output/dates' + str(i) + '.xlsx','output/dates_pretty' + str(i) + '.xlsx')


    # for i in range(200,240):
    #     data = multithreaded_iteration(data, config, 32, 4000, True)
    #     print("Score: ", data.score)
    #     data.save_to(year, 'output/dates' + str(i) + '.xlsx')
    #     convert_output('output/dates' + str(i) + '.xlsx','output/dates_pretty' + str(i) + '.xlsx')
    #
    # for i in range(240,280):
    #     data = multithreaded_iteration(data, config, 32, 10000, True)
    #     print("Score: ", data.score)
    #     data.save_to(year, 'output/dates' + str(i) + '.xlsx')
    #     convert_output('output/dates' + str(i) + '.xlsx','output/dates_pretty' + str(i) + '.xlsx')
    #
    # for i in range(280,300):
    #     data = multithreaded_iteration(data, config, 32, 20000, True)
    #     print("Score: ", data.score)
    #     data.save_to(year, 'output/dates' + str(i) + '.xlsx')
    #     convert_output('output/dates' + str(i) + '.xlsx','output/dates_pretty' + str(i) + '.xlsx')


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
