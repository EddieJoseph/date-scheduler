import numpy as np
import pandas as pd
from numpy import ndarray

from ej.scheduler.util.date_utils import convert_to_day_of_year
from ej.scheduler.util.row_names import RowNames, HolidayRowNames
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows, SamplingDataHolder


class JfHolidayEvaluator(Evaluator):

    def __init__(self, path: str):
        self.jf_type = None
        holidays = pd.read_excel(path)

        self.blocked_dates = []

        for index, row in holidays.iterrows():
            if row[HolidayRowNames.ONLY_JF.value]:
                start = convert_to_day_of_year(row[HolidayRowNames.START.value])
                end = convert_to_day_of_year(row[HolidayRowNames.END.value]) + 1
                for d in range(start, end):
                    self.blocked_dates.append(d)

    def set_jf_type(self, sampling_data_holder: SamplingDataHolder):
        self.jf_type = sampling_data_holder.map_types(['J'])[0]

    def evaluate(self, dates: pd.DataFrame) -> float:
        filtered_dates = dates[dates[RowNames.TYPE.value] == 'J']
        return 0.8 ** len(filtered_dates[(filtered_dates[RowNames.DATE.value].isin(self.blocked_dates))])

    def evaluate_np(self, dates: ndarray) -> float:
        jf_dates = dates[dates[:, SamplingRows.TYPE.value] == self.jf_type][:,SamplingRows.DATE.value]
        return 0.8 ** len(np.intersect1d(jf_dates, self.blocked_dates))

    def get_name(self) -> str:
        return "JfHolidayEvaluator"
