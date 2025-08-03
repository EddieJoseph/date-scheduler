import numpy as np
import pandas as pd
from numpy import ndarray

from ej.scheduler.util.date_utils import convert_to_day_of_year, filter_events
from ej.scheduler.util.row_names import RowNames, HolidayRowNames
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows, SamplingDataHolder

class JfHolidayEvaluator(Evaluator):

    def __init__(self, path: str, year: int):
        self.jf_type = None
        holidays = pd.read_excel(path)
        holidays = filter_events(holidays, year)
        self.blocked_dates = []

        for index, row in holidays.iterrows():
            if row[HolidayRowNames.ONLY_JF.value]:
                start = convert_to_day_of_year(row[HolidayRowNames.START.value])
                end = convert_to_day_of_year(row[HolidayRowNames.END.value]) + 1
                for d in range(start, end):
                    self.blocked_dates.append(d)

    def set_jf_type(self, sampling_data_holder: SamplingDataHolder):
        self.jf_type = sampling_data_holder.map_types(['J'])[0]

    def evaluate(self, dates: ndarray) -> float:
        dates_f = dates[dates[:, SamplingRows.FIXED.value] == 0]
        jf_dates = dates_f[dates_f[:, SamplingRows.TYPE.value] == self.jf_type][:,SamplingRows.DATE.value]
        return 0.8 ** len(np.intersect1d(jf_dates, self.blocked_dates))

    def get_name(self) -> str:
        return "JfHolidayEvaluator"
