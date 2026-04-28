import datetime

import numpy as np

from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows


class WeekClumpingEvaluator(Evaluator):
    def __init__(self, year):
        self.wd_offset = datetime.date(year, 1, 1).weekday()

    def evaluate(self, dates):
        weeks = np.unique((dates[:, SamplingRows.DATE.value] + self.wd_offset) // 7, return_counts=True)[1]
        tmp = 0.99 ** len(weeks[weeks > 2]) * 0.9 ** len(weeks[weeks > 3]) * 0.5 ** len(weeks[weeks > 5])
        return tmp

    def get_name(self) -> str:
        return "WeekClumpingEvaluator"
