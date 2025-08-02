import multiprocessing

import numpy as np

from ej.scheduler.generation.date_scheduler import iterate, print_details, \
    evaluate_candidate
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
from ej.scheduler.generation.sampling_data_holder import SamplingDataHolder
from ej.scheduler.plotter import Plotter
from ej.scheduler.reporting.excel.convert_output import convert_output
from ej.scheduler.util.scheduler_config import SchedulerData, SchedulerConfig


def worker(td):
    t_data = iterate(td[0], td[1], td[2], td[3])
    return t_data


def multithreaded_iteration(ti_data: SamplingDataHolder, ti_config, num_threads, num_iterations=1, limit=False):
    queue = multiprocessing.Queue()

    td = [(ti_data, ti_config, num_iterations, limit) for _ in range(num_threads)]
    with multiprocessing.Pool(processes=num_threads) as pool:
        results = pool.map(worker, td)
        best = results[0]
        for r in results:
            if r.get_score() > best.get_score():
                best = r
        return best


def plot_results(score, iterations, plotter, enabled: bool = True):
    if enabled:
        plotter.add_result(score, iterations)


def batch_iterations(data_np: SamplingDataHolder, iterations, repeat, limit_sampling, config, plotter, thread_nr,
                     log_msg=None, multithreaded=True, cycles=True):
    if log_msg is not None:
        print(log_msg)
    for i in range(repeat):
        if not multithreaded:
            data_np = iterate(data_np, config, iterations, limit_sampling)
            if not cycles:
                plot_results(data_np.get_score(), iterations, plotter)
            else:
                plot_results(data_np.get_score(), 1, plotter)
        else:
            data_np = multithreaded_iteration(data_np, config, thread_nr, iterations, limit_sampling)
            if not cycles:
                plot_results(data_np.get_score(), iterations * thread_nr, plotter)
            else:
                plot_results(data_np.get_score(), 1, plotter)
        print_details(data_np, config)
    return data_np


def optimize(input_file_path: str, holiday_file_path: str, output_file_prefix: str, year: int,
             random_seed: int | None = None, thread_nr: int = 32):
    if (random_seed is not None):
        np.random.seed(random_seed)
    plotter = Plotter()

    no_change_sampler = NoChangeDateSampler()
    small_sampler = NormalDateSampler(variance=3)
    medium_sampler = NormalDateSampler(variance=30)
    large_sampler = NormalDateSampler(variance=150)

    # sampler = CombinedSampler([no_change_sampler,small_sampler,medium_sampler,large_sampler],[0.9,0.2,0.07,0.03])
    sampler = FilteredCombinedSampler([small_sampler, medium_sampler, large_sampler],
                                      [0.6, 0.3, 0.1], year, holiday_file_path)

    type_spread_evaluator = TypeSpreadEvaluator()
    holiday_evaluator = HolidayEvaluator(holiday_file_path, year)
    jf_holiday_evaluator = JfHolidayEvaluator(holiday_file_path, year)
    as_evaluator = AsCleanEvaluator(year)
    weekend_evaluator = WeekendEvaluator(year)
    week_clumping_evaluator = WeekClumpingEvaluator(year)
    same_day_evaluator = SameDayEvaluator()
    month_evaluator = MonthEvaluator()
    assi_evaluator = AssiEvaluator()

    data = SchedulerData.create_from(input_file_path)
    config = SchedulerConfig(year, [type_spread_evaluator, as_evaluator, holiday_evaluator, weekend_evaluator,
                                    same_day_evaluator, jf_holiday_evaluator, week_clumping_evaluator, month_evaluator,
                                    assi_evaluator], sampler)
    data_np = SamplingDataHolder(data)

    type_spread_evaluator.set_types(data_np)
    jf_holiday_evaluator.set_jf_type(data_np)
    assi_evaluator.set_assi_types(data_np)

    data_np.set_score(evaluate_candidate(data_np.get_np_data(), config))
    print('Initial score: ', data_np.get_score())
    i = 1

    plot_results(data_np.get_score(), 0, plotter)
    data_np = batch_iterations(data_np, 25, 200, True, config, plotter, thread_nr, 'starting set ' + str(i))
    sd = data_np.get_scheduler_data()
    sd.save_to(year, output_file_prefix + str(i) + '.xlsx')
    convert_output(sd.dates, output_file_prefix + '_pretty' + str(i) + '.xlsx', 2025)
    i = i + 1

    data_np = batch_iterations(data_np, 5000, 1, True, config, plotter, thread_nr, 'starting set ' + str(i))
    sd = data_np.get_scheduler_data()
    sd.save_to(year, output_file_prefix + str(i) + '.xlsx')
    convert_output(sd.dates, output_file_prefix + '_pretty' + str(i) + '.xlsx', 2025)
    # i = i + 1
    data_np = batch_iterations(data_np, 50, 400, True, config, plotter, thread_nr, 'starting set ' + str(i))
    sd = data_np.get_scheduler_data()
    sd.save_to(year, output_file_prefix + str(i) + '.xlsx')
    convert_output(sd.dates, output_file_prefix + '_pretty' + str(i) + '.xlsx', 2025)
    i = i + 1

    data_np = batch_iterations(data_np, 5000, 10, True, config, plotter, thread_nr, 'starting set ' + str(i))
    sd = data_np.get_scheduler_data()
    sd.save_to(year, output_file_prefix + str(i) + '.xlsx')
    convert_output(sd.dates, output_file_prefix + '_pretty' + str(i) + '.xlsx', 2025)
    # i = i + 1
    data_np = batch_iterations(data_np, 100, 400, True, config, plotter, thread_nr, 'starting set ' + str(i))
    sd = data_np.get_scheduler_data()
    sd.save_to(year, output_file_prefix + str(i) + '.xlsx')
    convert_output(sd.dates, output_file_prefix + '_pretty' + str(i) + '.xlsx', 2025)
    i = i + 1

    data_np = batch_iterations(data_np, 5000, 30, True, config, plotter, thread_nr, 'starting set ' + str(i))
    sd = data_np.get_scheduler_data()
    sd.save_to(year, output_file_prefix + str(i) + '.xlsx')
    convert_output(sd.dates, output_file_prefix + '_pretty' + str(i) + '.xlsx', 2025)
    # i = i + 1
    data_np = batch_iterations(data_np, 200, 800, True, config, plotter, thread_nr, 'starting set ' + str(i))
    sd = data_np.get_scheduler_data()
    sd.save_to(year, output_file_prefix + str(i) + '.xlsx')
    convert_output(sd.dates, output_file_prefix + '_pretty' + str(i) + '.xlsx', 2025)
    i = i + 1

    data_np = batch_iterations(data_np, 10000, 5, True, config, plotter, thread_nr, 'starting set ' + str(i))
    sd = data_np.get_scheduler_data()
    sd.save_to(year, output_file_prefix + str(i) + '.xlsx')
    convert_output(sd.dates, output_file_prefix + '_pretty' + str(i) + '.xlsx', 2025)
    # i = i + 1

    for xyz in range(0, 1000):
        data_np = batch_iterations(data_np, 250, 500, True, config, plotter, thread_nr, 'starting set ' + str(i))
        sd = data_np.get_scheduler_data()
        sd.save_to(year, output_file_prefix + str(i) + '.xlsx')
        convert_output(sd.dates, output_file_prefix + '_pretty' + str(i) + '.xlsx', 2025)
        # i = i + 1

        data_np = batch_iterations(data_np, 10000, 10, True, config, plotter, thread_nr, 'starting set ' + str(i))
        sd = data_np.get_scheduler_data()
        sd.save_to(year, output_file_prefix + str(i) + '.xlsx')
        convert_output(sd.dates, output_file_prefix + '_pretty' + str(i) + '.xlsx', 2025)
        i = i + 1
