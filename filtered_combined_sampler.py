import numpy as np
import pandas as pd

from date_utils import convert_to_day_of_year, get_sundays_of_year
from sampler import Sampler


class FilteredCombinedSampler(Sampler):
    def __init__(self, samplers: [Sampler], weights: [float], year, holiday_path):
        if len(samplers) != len(weights):
            raise ValueError("samplers and weights must have the same length")
        if sum(weights) != 1:
            weights = [w / sum(weights) for w in weights]

        self.weights = weights
        self.samplers = samplers

        holidays = pd.read_excel(holiday_path)

        blocked_dates = []

        for index, row in holidays.iterrows():
            start = convert_to_day_of_year(row['start'])
            end = convert_to_day_of_year(row['end']) + 1
            for d in range(start, end):
                blocked_dates.append(d)

        self.blocked_dates = np.unique(np.concatenate([blocked_dates, get_sundays_of_year(year)]))

    def sample(self, date):
        sampler = np.random.choice(self.samplers, p=self.weights)
        new_date = sampler.sample(date)
        while new_date in self.blocked_dates:
            sampler = np.random.choice(self.samplers, p=self.weights)
            new_date = sampler.sample(date)
        return new_date