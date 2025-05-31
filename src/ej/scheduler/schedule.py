import multiprocessing

import numpy as np

from ej.scheduler.generation.date_scheduler import iterate, print_details, iterate_np, print_details_np
from ej.scheduler.generation.evaluation.as_clean_evaluator import AsCleanEvaluator
from ej.scheduler.generation.evaluation.assi_evaluator import AssiEvaluator
from ej.scheduler.generation.evaluation.holiday_evaluator import HolidayEvaluator
from ej.scheduler.generation.evaluation.jf_holiday_evaluator import JfHolidayEvaluator
from ej.scheduler.generation.evaluation.month_evaluator import MonthEvaluator
from ej.scheduler.generation.evaluation.same_day_evaluator import SameDayEvaluator
from ej.scheduler.generation.evaluation.type_spread_evaluator import TypeSpreadEvaluator
from ej.scheduler.generation.evaluation.week_clumping_evaluator import WeekClumpingEvaluator
from ej.scheduler.generation.evaluation.weekend_evaluator import WeekendEvaluator
from ej.scheduler.generation.sampling.filtered_combined_sampler import FilteredCombinedSampler
from ej.scheduler.generation.sampling.no_change_date_sampler import NoChangeDateSampler
from ej.scheduler.generation.sampling.normal_date_sampler import NormalDateSampler
from ej.scheduler.generation.sampling.uniform_sampler import UniformSampler
from ej.scheduler.generation.sampling_data_holder import SamplingDataHolder
from ej.scheduler.reporting.excel.convert_output import convert_output
from ej.scheduler.util.date_utils import get_week_days_of_year
from ej.scheduler.util.scheduler_config import SchedulerData, SchedulerConfig


def worker(td):
    t_data = iterate(td[0], td[1], td[2], td[3])
    return t_data

def worker_np(td):
    t_data = iterate_np(td[0], td[1], td[2], td[3])
    return t_data


def multithreaded_iteration(ti_data: SchedulerData, ti_config, num_threads, num_iterations=1, limit=False):
    queue = multiprocessing.Queue()

    td = [(ti_data, ti_config, num_iterations, limit) for _ in range(num_threads)]
    with multiprocessing.Pool(processes=num_threads) as pool:
        results = pool.map(worker, td)
        best = results[0]
        for r in results:
            if r.score > best.score:
                best = r
        return best

def multithreaded_iteration_np(ti_data: SamplingDataHolder, ti_config, num_threads, num_iterations=1, limit=False):
    queue = multiprocessing.Queue()

    td = [(ti_data, ti_config, num_iterations, limit) for _ in range(num_threads)]
    with multiprocessing.Pool(processes=num_threads) as pool:
        results = pool.map(worker_np, td)
        best = results[0]
        for r in results:
            if r.get_score() > best.get_score():
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
                                      [0.6, 0.3, 0.1], 2025, 'input/holidays.xlsx')
    initialization_sampler = UniformSampler()

    type_spread_evaluator = TypeSpreadEvaluator()
    holiday_evaluator = HolidayEvaluator('input/holidays.xlsx')
    jf_holiday_evaluator = JfHolidayEvaluator('input/holidays.xlsx')
    as_evaluator = AsCleanEvaluator(year)
    weekend_evaluator = WeekendEvaluator(year)
    week_clumping_evaluator = WeekClumpingEvaluator(year)
    same_day_evaluator = SameDayEvaluator()
    month_evaluator = MonthEvaluator()
    assi_evaluator = AssiEvaluator()

    # data = SchedulerData.create_from('input/best_input.xlsx')
    # data = SchedulerData.create_from('input/performance_test_easy.xlsx')
    data = SchedulerData.create_from('input/performance_test.xlsx')
    # config = SchedulerConfig.create_from('input/people.xlsx', year,
    #                                      [evaluator, holiday_evaluator, as_evaluator, weekend_evaluator,
    #                                       week_clumping_evaluator, same_day_evaluator, month_evaluator,
    #                                       jf_holiday_evaluator], sampler)
    config = SchedulerConfig.create_from('input/people.xlsx', year,
                                         [type_spread_evaluator, as_evaluator, holiday_evaluator, weekend_evaluator, same_day_evaluator, jf_holiday_evaluator, week_clumping_evaluator, month_evaluator, assi_evaluator], sampler)
    data_np = SamplingDataHolder(data)

    type_spread_evaluator.set_types(data_np)
    jf_holiday_evaluator.set_jf_type(data_np)
    assi_evaluator.set_assi_types(data_np)

    print('1st iteration')
    for i in range(100):
        # data_np = iterate_np(data_np, config, 1000, True)
        data_np = multithreaded_iteration_np(data_np, config, 32, 1000, True)
        print_details_np(data_np, config)
    print('2nd iteration')
    for i in range(25):
        # data_np = iterate_np(data_np, config, 2000, False)
        data_np = multithreaded_iteration_np(data_np, config, 32, 2000, False)
        print_details_np(data_np, config)
    print('3rd iteration')
    for i in range(100):
        # data_np = iterate_np(data_np, config, 1000, True)
        data_np = multithreaded_iteration_np(data_np, config, 32, 1000, True)
        print_details_np(data_np, config)
    print('4th iteration')
    for i in range(25):
        # data_np = iterate_np(data_np, config, 2000, False)
        data_np = multithreaded_iteration_np(data_np, config, 32, 2000, False)
        print_details_np(data_np, config)

    # for i in range(100):
    #     data_np = iterate_np(data_np, config, 1000, False)
    #     # data = multithreaded_iteration_np(data_np, config, 8, 1000, False)
    #     # print("Score: ", data.score)
    #     # print_details(data, config)
    #     print_details_np(data_np, config)
    #
    #     # sd = data.get_scheduler_data()
    #     # sd.save_to(year, 'output/dates' + str(i) + '.xlsx')
    #     # convert_output(sd.dates, 'output/dates_pretty' + str(i) + '.xlsx', 2025)


    # for i in range(5):
    #     # data = iterate(data, config, 500, True)
    #     data = multithreaded_iteration(data, config, 10, 100, True)
    #     # print("Score: ", data.score)
    #     # print_details(data, config)
    #     print_details(data, config)
    #
    #     data.save_to(year, 'output/dates' + str(i) + '.xlsx')
    #     convert_output(data.dates, 'output/dates_pretty' + str(i) + '.xlsx', 2025)

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
