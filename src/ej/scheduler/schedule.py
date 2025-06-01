import multiprocessing

import numpy as np

from ej.scheduler.generation.date_scheduler import iterate, print_details, iterate_np, print_details_np, \
    evaluate_candidate_np
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
from ej.scheduler.plotter import Plotter
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

def plot_results(score, iterations, enapled:bool=True):
    if enapled:
        plotter.add_result(score, iterations)


def batch_iterations(iterations,repeat,limit_sampling,log_msg=None,multithreaded=True):
    global data_np
    if(log_msg is not None):
        print(log_msg)
    for i in range(repeat):
        if not multithreaded:
            data_np = iterate_np(data_np, config, iterations, limit_sampling)
            plot_results(data_np.get_score(), iterations)
        else:
            data_np = multithreaded_iteration_np(data_np, config, thread_nr, iterations, limit_sampling)
            plot_results(data_np.get_score(), iterations * thread_nr)
        print_details_np(data_np, config)


if __name__ == '__main__':
    np.random.seed(74587)
    year = 2025
    get_week_days_of_year(year)
    thread_nr=32
    plotter = Plotter()

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

    data = SchedulerData.create_from('input/performance_test.xlsx')
    config = SchedulerConfig.create_from('input/people.xlsx', year,
                                         [type_spread_evaluator, as_evaluator, holiday_evaluator, weekend_evaluator, same_day_evaluator, jf_holiday_evaluator, week_clumping_evaluator, month_evaluator, assi_evaluator], sampler)
    data_np = SamplingDataHolder(data)
    data_np.set_score(evaluate_candidate_np(data_np.get_np_data(),config))

    type_spread_evaluator.set_types(data_np)
    jf_holiday_evaluator.set_jf_type(data_np)
    assi_evaluator.set_assi_types(data_np)

    print('Initial score: ', data_np.get_score())
    i=1

    plot_results(data_np.get_score(), 0)
    batch_iterations(25, 100, True, 'starting set ' + str(i))
    sd = data_np.get_scheduler_data()
    sd.save_to(year, 'output/dates' + str(i) + '.xlsx')
    convert_output(sd.dates, 'output/dates_pretty' + str(i) + '.xlsx', 2025)
    i = i + 1

    plot_results(data_np.get_score(), 0)
    batch_iterations(100, 50, True, 'starting set ' + str(i))
    sd = data_np.get_scheduler_data()
    sd.save_to(year, 'output/dates' + str(i) + '.xlsx')
    convert_output(sd.dates, 'output/dates_pretty' + str(i) + '.xlsx', 2025)
    i = i + 1

    plot_results(data_np.get_score(),0)
    batch_iterations(200,25, True, 'starting set ' + str(i))
    sd = data_np.get_scheduler_data()
    sd.save_to(year, 'output/dates' + str(i) + '.xlsx')
    convert_output(sd.dates, 'output/dates_pretty' + str(i) + '.xlsx', 2025)
    i=i+1

    for xyz in range(0,100):
        plot_results(data_np.get_score(), 0)
        batch_iterations(300, 20, True, 'starting set ' + str(i))
        sd = data_np.get_scheduler_data()
        sd.save_to(year, 'output/dates' + str(i) + '.xlsx')
        convert_output(sd.dates, 'output/dates_pretty' + str(i) + '.xlsx', 2025)
        i = i + 1

        plot_results(data_np.get_score(), 0)
        batch_iterations(1000, 5, True, 'starting set ' + str(i))
        sd = data_np.get_scheduler_data()
        sd.save_to(year, 'output/dates' + str(i) + '.xlsx')
        convert_output(sd.dates, 'output/dates_pretty' + str(i) + '.xlsx', 2025)
        i = i + 1

