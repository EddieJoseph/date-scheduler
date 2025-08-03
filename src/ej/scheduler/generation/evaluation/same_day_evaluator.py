import numpy as np

from ej.scheduler.util.row_names import RowNames
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows, SamplingDataHolder


class SameDayEvaluator(Evaluator):

    def __init__(self):
        self.info_type = None

    def set_info_type(self, sampling_data_holder: SamplingDataHolder):
        self.info_type = sampling_data_holder.map_types(['INFO'])[0]

    def evaluate(self, dates):
        dates_f = dates[dates[:, SamplingRows.TYPE.value] != self.info_type]
        ex_per_day = np.unique(dates_f[:, SamplingRows.DATE.value],return_counts=True)[1]
        ex_per_day_c = len(ex_per_day[ex_per_day > 1])
        return 0.3 ** ex_per_day_c

    def get_name(self) -> str:
        return "SameDayEvaluator"
