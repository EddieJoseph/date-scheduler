import numpy as np

from date_utils import get_saturdays_of_year, get_sundays_of_year
from evaluator import Evaluator
from row_names import RowNames


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
        c = len(sat_dates)-len(sat_dates[sat_dates.isin(self.saturdays)])

        tmp = 0.6**(a+b+c)
        return tmp