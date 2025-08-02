import numpy as np

from ej.scheduler.util.row_names import RowNames
from .evaluator import Evaluator
from ..sampling_data_holder import SamplingDataHolder, SamplingRows

def generate_score_np(indexes1, indexes2, dates):
    comb_ind = np.intersect1d(indexes1, indexes2)
    if len(comb_ind) < 2:
        return 1
    dates_filtered = dates[comb_ind]
    diffs = np.diff(dates_filtered, append=dates_filtered[0] + 365)
    result = 1 / (1 + np.sqrt(np.var(diffs) / 10000))
    return result


class TypeSpreadEvaluator(Evaluator):
    excluded_types = ["ST", "WTA", "SAN", "HY", "B", "ASSITST", "IFA", "MS", "KS", "SPEZ"]
    types = []

    def set_types(self, sampling_data_holder: SamplingDataHolder):
        self.types = sampling_data_holder.map_types([type for type in sampling_data_holder.get_types() if type not in self.excluded_types])

    def evaluate(self, candidate):
        result = 1
        gb = np.where(candidate[:,SamplingRows.GB.value] == 1)[0]
        kb = np.where(candidate[:,SamplingRows.KB.value] == 1)[0]
        rb = np.where(candidate[:,SamplingRows.RB.value] == 1)[0]
        ng = np.where((candidate[:,SamplingRows.GB.value] == 0) & (candidate[:,SamplingRows.KB.value] == 0) & (candidate[:,SamplingRows.RB.value] == 0))[0]

        dates = candidate[:,SamplingRows.DATE.value]

        for type in self.types:
            t = np.where(candidate[:,SamplingRows.TYPE.value] == type)[0]
            result *= (generate_score_np(t, gb, dates)
                       * generate_score_np(t, kb, dates)
                       * generate_score_np(t, rb, dates)
                       * generate_score_np(t, ng, dates))
        return result

    def get_name(self) -> str:
        return "TypeSpreadEvaluator"
