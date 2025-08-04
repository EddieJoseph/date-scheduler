from datetime import datetime

import numpy as np
from numpy import ndarray

from .evaluator import Evaluator
from ..sampling_data_holder import SamplingDataHolder, SamplingRows


class WeekDayEvaluator(Evaluator):
    
    def __init__(self, year: int):
        self.year = year
        first_day = datetime(year, 1, 1)
        self.offset = first_day.weekday()
        self.types = []

    def add_type(self,type_name:str, sampling_data_holder: SamplingDataHolder):
        self.types.append(sampling_data_holder.map_types([type_name])[0])

    def get_week_day(self, day):
        return (day + self.offset) % 7

    def evaluate_type(self, dates: ndarray) -> float:
        weekdays =  np.array([self.get_week_day(date) for date in dates[:, SamplingRows.DATE.value]])
        filtered_weekdays = weekdays[weekdays < 4]
        if len(filtered_weekdays)<1:
            return 1.0
        weekday_count = np.bincount(filtered_weekdays,minlength=4)
        result = 1 / (1 + np.sqrt(np.var(weekday_count) / 10))
        return result

    def evaluate(self, dates:ndarray) -> float:
        result = 1.0
        for t in self.types:
            dates_f = dates[dates[:,SamplingRows.TYPE.value] == t]
            dates_rb = dates_f[dates_f[:,SamplingRows.RB.value] == 1]
            result *= self.evaluate_type(dates_rb)
            dates_kb = dates_f[dates_f[:,SamplingRows.KB.value] == 1]
            result *= self.evaluate_type(dates_kb)
            dates_gb = dates_f[dates_f[:,SamplingRows.GB.value] == 1]
            result *= self.evaluate_type(dates_gb)

        return result

    def get_name(self) -> str:
        return "WeekDayEvaluator"
        
        