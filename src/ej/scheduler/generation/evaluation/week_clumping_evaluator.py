import datetime

import numpy as np

from ej.scheduler.util.row_names import RowNames
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows


class WeekClumpingEvaluator(Evaluator):
    def __init__(self, year):
        self.wd_offset = datetime.date(year, 1, 1).weekday()
        self.vectorized_get_week = np.vectorize(self.get_week)

    def get_week(self, day):
        return np.floor((day + self.wd_offset) / 7).astype(int)

    def evaluate(self, dates):
        weeks = np.unique(self.vectorized_get_week(dates[:, SamplingRows.DATE.value]),return_counts=True)[1]
        tmp = 0.99 ** len(weeks[weeks > 2]) * 0.9 ** len(weeks[weeks > 3]) * 0.5 ** len(weeks[weeks > 5])
        return tmp

    def get_name(self) -> str:
        return "WeekClumpingEvaluator"
