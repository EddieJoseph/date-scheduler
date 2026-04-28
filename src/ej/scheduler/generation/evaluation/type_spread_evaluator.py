import numpy as np

from .evaluator import Evaluator
from ..sampling_data_holder import SamplingDataHolder, SamplingRows


def generate_score_np(dates_filtered):
    if len(dates_filtered) < 2:
        return 1
    diffs = np.diff(dates_filtered, append=dates_filtered[0] + 365)
    result = 1 / (1 + np.sqrt(np.var(diffs) / 10000))
    return result


class TypeSpreadEvaluator(Evaluator):
    excluded_types = ["ST", "WTA", "SAN", "HY", "B", "ASSITST", "IFA", "MS", "KS", "SPEZ"]
    types = []

    def set_types(self, sampling_data_holder: SamplingDataHolder):
        self.types = sampling_data_holder.map_types(
            [t for t in sampling_data_holder.get_types() if t not in self.excluded_types]
        )

    def evaluate(self, candidate):
        result = 1
        mask_gb = candidate[:, SamplingRows.GB.value] == 1
        mask_kb = candidate[:, SamplingRows.KB.value] == 1
        mask_rb = candidate[:, SamplingRows.RB.value] == 1
        mask_ng = ~mask_gb & ~mask_kb & ~mask_rb

        dates = candidate[:, SamplingRows.DATE.value]

        for t in self.types:
            mask_type = candidate[:, SamplingRows.TYPE.value] == t
            result *= (generate_score_np(dates[mask_type & mask_gb])
                       * generate_score_np(dates[mask_type & mask_kb])
                       * generate_score_np(dates[mask_type & mask_rb])
                       * generate_score_np(dates[mask_type & mask_ng]))
        return result

    def get_name(self) -> str:
        return "TypeSpreadEvaluator"
