import time

import numpy as np

from ej.scheduler.generation.sampling_data_holder import SamplingDataHolder, sort_np_data_by_date
from ej.scheduler.util.scheduler_config import SchedulerConfig


def evaluate_candidate(candidate: np.ndarray, config: SchedulerConfig):
    total = 1
    for evaluator in config.evaluators:
        total *= evaluator.evaluate(candidate)
    return total

time_counter = 0
timers = {}

def evaluate_candidate_timed(candidate: np.ndarray, config: SchedulerConfig):
    global time_counter
    time_counter += 1
    total = 1
    for evaluator in config.evaluators:
        start = time.time()
        total *= evaluator.evaluate(candidate)
        end = time.time()
        timers[evaluator.get_name()] = timers.get(evaluator.get_name(), 0) + end - start
    return total


def print_timers():
    total = 0
    for key in timers:
        total += timers[key] / time_counter

    for key in timers:
        print(key + "\t" + str(timers[key] / time_counter) + "\t" + str(timers[key] / time_counter / total) + "%")

def generate_candidate(dates: np.ndarray, config: SchedulerConfig, limit_randomness=False) -> tuple[np.ndarray, set[int]]:
    candidate, changed_indices = config.sampler.sample(dates)
    return sort_np_data_by_date(candidate), changed_indices


def print_evaluation(max, max_p, cand, cand_p, config: SchedulerConfig, accept, reject):
    var = "{:.2E}".format(cand_p) + ";" + str(accept / (accept + reject)) + ";" + "{:.2E}".format(max_p)
    for evaluator in config.evaluators:
        var = var + ";" + type(evaluator).__name__ + " :" + "{:.2E}".format(evaluator.evaluate(cand))
    print(var)

def print_details(data: SamplingDataHolder, config: SchedulerConfig):
    var = "Score: {:.6E}".format(data.get_score())
    for evaluator in config.evaluators:
        var = var + "\t" + type(evaluator).__name__ + " :" + "{:.2E}".format(evaluator.evaluate(data.get_np_data()))
    print(var)

def iterate(data: SamplingDataHolder, config: SchedulerConfig, iterations=1, limit=False):
    accepted_p = evaluate_candidate(data.get_np_data(), config)
    data.set_score(accepted_p)
    accepted = data.get_np_data()
    accept = 0
    reject = 0
    caches: list[dict[int, float]] = [{} for _ in config.evaluators]

    for i in range(iterations):
        cand, changed_indices = generate_candidate(accepted, config, limit_randomness=limit)
        cand_p = 1.0
        new_caches = []
        for j, evaluator in enumerate(config.evaluators):
            score, new_cache = evaluator.evaluate_incremental(cand, changed_indices, caches[j])
            cand_p *= score
            new_caches.append(new_cache)

        if cand_p > data.get_score():
            data.set_score(cand_p)
            data.set_np_data(cand)

        if min(1.0, cand_p / accepted_p) > np.random.rand()**0.7:
            accepted = cand
            accepted_p = cand_p
            caches = new_caches
            accept += 1
        else:
            reject += 1
    return data
