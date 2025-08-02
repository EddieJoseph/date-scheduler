import numpy as np
import pandas as pd
from numpy import ndarray

from ej.scheduler.util.date_utils import convert_to_day_of_year
from ej.scheduler.util.row_names import RowNames, HolidayRowNames
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows


class HolidayEvaluator(Evaluator):

    def __init__(self, path: str):
        holidays = pd.read_excel(path)

        self.blocked_dates = []

        for index, row in holidays.iterrows():
            if not row[HolidayRowNames.ONLY_JF.value]:
                start = convert_to_day_of_year(row[HolidayRowNames.START.value])
                end = convert_to_day_of_year(row[HolidayRowNames.END.value]) + 1
                for d in range(start, end):
                    self.blocked_dates.append(d)

    def evaluate(self, dates: ndarray) -> float:
        return 0.8 ** len(np.intersect1d(dates[:,SamplingRows.DATE.value], self.blocked_dates))

    def get_name(self) -> str:
        return "HolidayEvaluator"
