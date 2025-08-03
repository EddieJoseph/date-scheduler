import numpy as np

from ej.scheduler.util.date_utils import get_month_from_day_of_year
from ej.scheduler.util.row_names import RowNames
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows


class MonthEvaluator(Evaluator):

    def __init__(self):
        self.vectorized_get_month = np.vectorize(get_month_from_day_of_year)

    def evaluate(self, dates):
        filtered = dates[dates[:, SamplingRows.MONTH.value] != -1]
        dates_f = filtered[filtered[:, SamplingRows.FIXED.value] == 0]
        months = self.vectorized_get_month(dates_f[:,SamplingRows.DATE.value])
        diff = dates_f[:,SamplingRows.MONTH.value] - months
        violations = np.sum(np.abs(diff))

        return 0.85 ** violations

    def get_name(self) -> str:
        return "MonthEvaluator"
