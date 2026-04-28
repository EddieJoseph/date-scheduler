from typing import List

import numpy as np
import pandas as pd

from ej.scheduler.generation.sampling_data_holder import SamplingRows, change_date
from ej.scheduler.util.date_utils import convert_to_day_of_year, get_sundays_of_year, get_fridays_of_year, filter_events
from .sampler import Sampler


class FilteredCombinedSampler(Sampler):
    def __init__(self, samplers: List[Sampler], weights: List[float], year, holiday_path):
        if len(samplers) != len(weights):
            raise ValueError("samplers and weights must have the same length")
        if sum(weights) != 1:
            weights = [w / sum(weights) for w in weights]

        self.weights = weights
        self.samplers = samplers

        holidays = filter_events(pd.read_excel(holiday_path),year)

        blocked_dates = []

        for index, row in holidays.iterrows():
            if not row['only_jf']:
                start = convert_to_day_of_year(row['start'])
                end = convert_to_day_of_year(row['end']) + 1
                for d in range(start, end):
                    blocked_dates.append(d)

        self.blocked_dates = np.unique(np.concatenate([blocked_dates, get_sundays_of_year(year), get_fridays_of_year(year)]))

    def sample(self, candidate: np.ndarray) -> tuple[np.ndarray, set[int]]:
        not_fixed = np.where(candidate[:, SamplingRows.FIXED.value] == 0)[0]
        if len(not_fixed) == 0:
            return candidate, set()
        idx = int(np.random.choice(not_fixed))
        original_date = int(candidate[idx, SamplingRows.DATE.value])

        sampler = np.random.choice(self.samplers, p=self.weights)
        new_date = sampler._sample_date(original_date)
        while new_date in self.blocked_dates:
            sampler = np.random.choice(self.samplers, p=self.weights)
            new_date = sampler._sample_date(original_date)

        new_candidate = candidate.copy()
        change_date(new_candidate, idx, new_date)
        return new_candidate, {idx}
