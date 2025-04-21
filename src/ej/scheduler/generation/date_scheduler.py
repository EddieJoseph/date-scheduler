import time

import numpy as np
from pandas import DataFrame

from ej.scheduler.generation.sampling_data_holder import SamplingDataHolder, SamplingRows, change_date, \
    sort_np_data_by_date, switch_dates
from ej.scheduler.util.row_names import RowNames
from ej.scheduler.util.scheduler_config import SchedulerData, SchedulerConfig


def evaluate_candidate(candidate: DataFrame, config: SchedulerConfig):
    total = 1
    for evaluator in config.evaluators:
        total *= evaluator.evaluate(candidate)
    return total

def evaluate_candidate_np(candidate: np.ndarray, config: SchedulerConfig):
    total = 1
    for evaluator in config.evaluators:
        total *= evaluator.evaluate_np(candidate)
    return total


time_counter = 0
timers = {}


def evaluate_candidate_timed(candidate: DataFrame, config: SchedulerConfig):
    global time_counter
    time_counter += 1
    total = 1
    for evaluator in config.evaluators:
        start = time.time()
        total *= evaluator.evaluate(candidate)
        end = time.time()
        timers[evaluator.get_name()] = timers.get(evaluator.get_name(), 0) + end - start
    return total

def evaluate_candidate_timed_np(candidate: np.ndarray, config: SchedulerConfig):
    global time_counter
    time_counter += 1
    total = 1
    for evaluator in config.evaluators:
        start = time.time()
        total *= evaluator.evaluate_np(candidate)
        end = time.time()
        timers[evaluator.get_name()] = timers.get(evaluator.get_name(), 0) + end - start
    return total


def print_timers():
    total = 0
    for key in timers:
        total += timers[key] / time_counter

    for key in timers:
        print(key + "\t" + str(timers[key] / time_counter) + "\t" + str(timers[key] / time_counter / total) + "%")


def generate_candidate(dates: DataFrame, config: SchedulerConfig, limit_randomness=False):
    if not limit_randomness:
        candidate = dates.copy()
        for index, row in candidate.iterrows():
            if not row[RowNames.FIXED.value]:
                candidate.loc[index, RowNames.DATE.value] = config.sampler.sample(row[RowNames.DATE.value])
        return candidate.sort_values(by=RowNames.DATE.value, inplace=False)
    else:
        not_fixed_indices = dates[dates[RowNames.FIXED.value] == False].index
        rows_to_change = np.random.choice(not_fixed_indices, np.random.randint(1, min(len(not_fixed_indices) + 1, 4)),
                                          replace=False)
        candidate = dates.copy()
        if len(rows_to_change) == 2 and np.random.randint(10) < 5:
            candidate.loc[rows_to_change[0], RowNames.DATE.value] = dates.loc[rows_to_change[1], RowNames.DATE.value]
            candidate.loc[rows_to_change[1], RowNames.DATE.value] = dates.loc[rows_to_change[0], RowNames.DATE.value]
        else:
            for index in rows_to_change:
                candidate.loc[index, RowNames.DATE.value] = config.sampler.sample(
                    candidate.loc[index, RowNames.DATE.value])
        return candidate.sort_values(by=RowNames.DATE.value, inplace=False)

def generate_candidate_np(dates: np.ndarray, config: SchedulerConfig, limit_randomness=False):
    if not limit_randomness:
        candidate = dates.copy()
        for i in range(len(candidate)):
            if candidate[i, SamplingRows.FIXED.value] == 0:
                change_date(candidate,config.sampler.sample(candidate[i, SamplingRows.DATE.value]))
        return sort_np_data_by_date(candidate)
    else:
        not_fixed_indices = np.where(dates[:,SamplingRows.FIXED.value] == 0)[0]
        rows_to_change = np.random.choice(not_fixed_indices, np.random.randint(1, min(len(not_fixed_indices) + 1, 4)),
                                          replace=False)
        candidate = dates.copy()
        if len(rows_to_change) == 2 and np.random.randint(10) < 5:
            switch_dates(candidate,rows_to_change[0],rows_to_change[1])
        else:
            for index in rows_to_change:
                change_date(candidate, index,config.sampler.sample(candidate[index, SamplingRows.DATE.value]))
        return sort_np_data_by_date(candidate)


def print_evaluation(max, max_p, cand, cand_p, config: SchedulerConfig, accept, reject):
    var = "{:.2E}".format(cand_p) + ";" + str(accept / (accept + reject)) + ";" + "{:.2E}".format(max_p)
    for evaluator in config.evaluators:
        var = var + ";" + type(evaluator).__name__ + " :" + "{:.2E}".format(evaluator.evaluate(cand))
    print(var)


def print_details(data: SchedulerData, config: SchedulerConfig):
    var = "Score: {:.6E}".format(data.score)
    for evaluator in config.evaluators:
        var = var + "\t" + type(evaluator).__name__ + " :" + "{:.2E}".format(evaluator.evaluate(data.dates))
    print(var)

def print_details_np(data: SamplingDataHolder, config: SchedulerConfig):
    var = "Score: {:.6E}".format(data.get_score())
    for evaluator in config.evaluators:
        var = var + "\t" + type(evaluator).__name__ + " :" + "{:.2E}".format(evaluator.evaluate_np(data.get_np_data()))
    print(var)


def iterate(data: SchedulerData, config: SchedulerConfig, iterations=1, limit=False):
    accepted_p = evaluate_candidate(data.dates, config)
    data.score = accepted_p
    accepted = data.dates.copy()
    # cand = data.dates.copy()
    accept = 0
    reject = 0
    for i in range(iterations):
        cand = generate_candidate(accepted, config, limit_randomness=limit)
        cand_p = evaluate_candidate(cand, config)

        if cand_p > data.score:
            data.score = cand_p
            data.dates = cand

        if min(1.0, cand_p / accepted_p) > np.random.rand():
            accepted = cand
            accepted_p = cand_p
            accept += 1
        else:
            reject += 1
        # if(i % 20 == 0):
        #     print(accepted_p)
    # print_evaluation(data.dates, data.score, accepted, accepted_p, config, accept, reject)
    # print_timers()
    return data

def iterate_np(data: SamplingDataHolder, config: SchedulerConfig, iterations=1, limit=False):
    accepted_p = evaluate_candidate_np(data.get_np_data(), config)
    data.set_score(accepted_p)
    accepted = data.get_np_data()
    accept = 0
    reject = 0
    for i in range(iterations):
        cand = generate_candidate_np(accepted, config, limit_randomness=limit)
        cand_p = evaluate_candidate_np(cand, config)

        if cand_p > data.get_score():
            data.set_score(cand_p)
            data.set_np_data(cand)

        if min(1.0, cand_p / accepted_p) > np.random.rand():
            accepted = cand
            accepted_p = cand_p
            accept += 1
        else:
            reject += 1
        # if(i % 20 == 0):
        #     print(accepted_p)
    # print_evaluation(data.dates, data.score, accepted, accepted_p, config, accept, reject)
    # print_timers()
    return data
