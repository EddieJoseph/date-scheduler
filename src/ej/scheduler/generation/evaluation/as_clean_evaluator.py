from abc import ABC

import numpy as np

from ej.scheduler.util.date_utils import get_week_days_of_year
from ej.scheduler.util.row_names import RowNames
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows

class AsCleanEvaluator(Evaluator):
    def __init__(self, year):
        self.week_days = get_week_days_of_year(year)
        self.min_days = 3

    def compare(self, d1, d2):
        tmp = len(self.week_days[(self.week_days >= d1) & (self.week_days < d2)])
        return tmp

    def get_diff_np(self, as_dates):
        differences = np.empty(len(as_dates) - 1, dtype=np.int16)
        for i in range(len(as_dates) - 1):
            diff_result = self.compare(as_dates[i], as_dates[i + 1])
            differences[i] = diff_result
        return differences

    def evaluate(self, dates):
        as_dates = dates[dates[:, SamplingRows.AS.value] == 1][:, SamplingRows.DATE.value]
        if len(as_dates) < 2:
            return 1
        diff = self.get_diff_np(as_dates)
        tmp = 0.6 ** len(diff[diff < self.min_days])
        return tmp

    def get_name(self) -> str:
        return "AsCleanEvaluator"
