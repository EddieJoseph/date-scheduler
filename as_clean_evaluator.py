import numpy as np

from date_utils import get_week_days_of_year
from evaluator import Evaluator


class AsCleanEvaluator(Evaluator):
    def __init__(self, year):
        self.week_days = get_week_days_of_year(year)
        self.min_days = 3

    def compare(self, d1, d2):
        tmp = len(self.week_days[(self.week_days >= d1) & (self.week_days < d2)])
        return tmp

    def get_diff(self, as_dates):
        differences = np.empty(len(as_dates) - 1, dtype=int)
        for i in range(len(as_dates) - 1):
            diff_result = self.compare(as_dates.values[i], as_dates.values[i + 1])
            differences[i] = diff_result
        return differences


    def evaluate(self, dates):
        as_dates = dates[dates['as'] == True]['date']
        diff = self.get_diff(as_dates)
        tmp = 0.8**len(diff[diff < self.min_days])
        return tmp
