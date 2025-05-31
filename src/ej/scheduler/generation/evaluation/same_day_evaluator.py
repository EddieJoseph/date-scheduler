import numpy as np

from ej.scheduler.util.row_names import RowNames
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows


class SameDayEvaluator(Evaluator):

    def evaluate(self, dates):
        # Evaluate the model on the same day data

        ex_per_day = dates[RowNames.DATE.value].value_counts()
        ex_per_day_c = len(ex_per_day[ex_per_day > 1])
        return 0.3 ** ex_per_day_c

    def evaluate_np(self, dates):
        ex_per_day = np.unique(dates[:, SamplingRows.DATE.value],return_counts=True)[1]
        ex_per_day_c = len(ex_per_day[ex_per_day > 1])
        return 0.3 ** ex_per_day_c

    def get_name(self) -> str:
        return "SameDayEvaluator"
