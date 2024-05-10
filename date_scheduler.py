import numpy as np
from pandas import DataFrame

from scheduler_config import SchedulerData, SchedulerConfig


def evaluate_candidate(candidate: DataFrame, config: SchedulerConfig):
    total = 1
    for evaluator in config.evaluators:
        total *= evaluator.evaluate(candidate)
    return total


def generate_candidate(dates: DataFrame, config: SchedulerConfig, limit_randomness=False):
    if not limit_randomness:
        candidate = dates.copy()
        for index, row in candidate.iterrows():
            candidate.loc[index, 'date'] = config.sampler.sample(row['date'])
        # sort candidate by date ascending
        return candidate.sort_values(by='date', inplace=False)
    else:
        rows_to_change = np.random.randint(0, len(dates), np.random.randint(1, 4))
        candidate = dates.copy()
        if len(rows_to_change) == 2 and np.random.randint(10) < 1:
            candidate.loc[rows_to_change[0], 'date'] = candidate.loc[rows_to_change[1], 'date']
            candidate.loc[rows_to_change[1], 'date'] = candidate.loc[rows_to_change[0], 'date']
        else:
            for index in rows_to_change:
                candidate.loc[index, 'date'] = config.sampler.sample(candidate.loc[index, 'date'])
        return candidate.sort_values(by='date', inplace=False)


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


def iterate(data: SchedulerData, config: SchedulerConfig, iterations=1, limit=False):
    accepted_p = evaluate_candidate(data.dates, config)
    data.score = accepted_p
    accepted = data.dates.copy()
    cand = data.dates.copy()
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
    return data
