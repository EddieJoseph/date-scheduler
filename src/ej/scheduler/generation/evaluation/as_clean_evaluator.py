import numpy as np

from ej.scheduler.util.date_utils import get_week_days_of_year
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows


class AsCleanEvaluator(Evaluator):
    def __init__(self, year):
        self.week_days = get_week_days_of_year(year)
        self.min_days = 3

    def get_diff_np(self, as_dates):
        return (np.searchsorted(self.week_days, as_dates[1:])
                - np.searchsorted(self.week_days, as_dates[:-1]))

    def evaluate(self, dates):
        as_dates = dates[dates[:, SamplingRows.AS.value] == 1][:, SamplingRows.DATE.value]
        if len(as_dates) < 2:
            return 1
        diff = self.get_diff_np(as_dates)
        tmp = 0.6 ** len(diff[diff < self.min_days])
        return tmp

    def get_name(self) -> str:
        return "AsCleanEvaluator"
