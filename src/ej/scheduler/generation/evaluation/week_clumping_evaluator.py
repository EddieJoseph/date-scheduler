import datetime

import numpy as np

from ej.scheduler.util.row_names import RowNames
from .evaluator import Evaluator


class WeekClumpingEvaluator(Evaluator):
    def __init__(self, year):
        self.wd_offset = datetime.date(year, 1, 1).weekday()

    def get_week(self, day):
        return np.floor((day + self.wd_offset) / 7).astype(int)

    def evaluate(self, dates):
        weeks = dates[RowNames.DATE.value].apply(self.get_week).value_counts()
        tmp = 0.99 ** len(weeks[weeks > 2]) * 0.9 ** len(weeks[weeks > 3]) * 0.5 ** len(weeks[weeks > 5])
        return tmp

    def get_name(self) -> str:
        return "WeekClumpingEvaluator"
