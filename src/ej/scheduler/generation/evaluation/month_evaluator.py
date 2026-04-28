import numpy as np

from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows

_MONTH_BOUNDS = np.array([31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334])


class MonthEvaluator(Evaluator):

    def evaluate(self, dates):
        filtered = dates[dates[:, SamplingRows.MONTH.value] != -1]
        dates_f = filtered[filtered[:, SamplingRows.FIXED.value] == 0]
        months = np.searchsorted(_MONTH_BOUNDS, dates_f[:, SamplingRows.DATE.value], side='right') + 1
        diff = dates_f[:, SamplingRows.MONTH.value] - months
        violations = np.sum(np.abs(diff))

        return 0.85 ** violations

    def get_name(self) -> str:
        return "MonthEvaluator"
