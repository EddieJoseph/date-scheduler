import numpy as np

from ej.scheduler.util.date_utils import get_saturdays_of_year, get_sundays_of_year, get_fridays_of_year
from ej.scheduler.util.row_names import RowNames
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows


class WeekendEvaluator(Evaluator):
    def __init__(self, year):
        self.year = year
        self.fridays = get_fridays_of_year(year)
        self.saturdays = get_saturdays_of_year(year)
        self.sundays = get_sundays_of_year(year)
        self.non_sat_weekend = np.concatenate((self.fridays, self.sundays))
        self.weekend = np.concatenate((self.fridays, self.saturdays, self.sundays))

    def evaluate(self, dates):
        dates_f = dates[dates[:, SamplingRows.FIXED.value] == 0]
        sat_dates = dates_f[dates_f[:,SamplingRows.SAT.value]==1][:,SamplingRows.DATE.value]
        not_sat_dates = dates_f[dates_f[:,SamplingRows.SAT.value]!=1][:,SamplingRows.DATE.value]
        a = len(np.intersect1d(not_sat_dates, self.weekend))
        b = len(sat_dates) - len(np.intersect1d(sat_dates, self.saturdays))

        tmp = 0.6 ** (a + b)
        return tmp

    def get_name(self) -> str:
        return "WeekendEvaluator"
