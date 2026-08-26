import numpy as np

from .evaluator import Evaluator
from ..sampling_data_holder import SamplingRows


class AssiEvaluator(Evaluator):

    def __init__(self):
        self.assi_types = None

    def set_assi_types(self, sampling_data_holder):
        self.assi_types = sampling_data_holder.map_types(['ASI', 'ASIKVK'])

    def evaluate(self, candidate):
        assi_dates = candidate[np.isin(candidate[:,SamplingRows.TYPE.value], self.assi_types)]
        assi_dates = assi_dates[assi_dates[:, SamplingRows.ORDER.value] != -1]
        if len(assi_dates) < 2:
            return 1.0
        sorted_by_date = assi_dates[np.argsort(assi_dates[:, SamplingRows.DATE.value])]
        diffs = np.diff(sorted_by_date[:, SamplingRows.ORDER.value])
        violations = len(diffs[diffs < 0])
        return 0.5 ** violations

    def get_name(self) -> str:
        return "AssiEvaluator"
