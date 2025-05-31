import numpy as np

from ej.scheduler.util.date_utils import get_saturdays_of_year, get_sundays_of_year
from ej.scheduler.util.row_names import RowNames
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows


class WeekendEvaluator(Evaluator):
    def __init__(self, year):
        self.year = year
        self.saturdays = get_saturdays_of_year(year)
        self.sundays = get_sundays_of_year(year)
        self.weekend = np.concatenate((self.saturdays, self.sundays))

    def evaluate(self, dates):
        sat_dates = dates[dates[RowNames.SAT.value] == True][RowNames.DATE.value]
        not_sat_dates = dates[dates[RowNames.SAT.value] == False][RowNames.DATE.value]

        a = len(not_sat_dates[not_sat_dates.isin(self.weekend)])
        b = len(sat_dates[sat_dates.isin(self.sundays)])
        c = len(sat_dates) - len(sat_dates[sat_dates.isin(self.saturdays)])

        tmp = 0.6 ** (a + b + c)
        return tmp

    def evaluate_np(self, dates):
        sat_dates = dates[dates[:,SamplingRows.SAT.value]==1][:,SamplingRows.DATE.value]
        not_sat_dates = dates[dates[:,SamplingRows.SAT.value]!=1][:,SamplingRows.DATE.value]
        a = len(np.intersect1d(not_sat_dates, self.weekend))
        b = len(np.intersect1d(sat_dates, self.saturdays))
        # c = len(np.intersect1d(sat_dates, self.sundays))

        # tmp = 0.6 ** (a + b + c)
        tmp = 0.6 ** (a + b)
        return tmp

    def get_name(self) -> str:
        return "WeekendEvaluator"
