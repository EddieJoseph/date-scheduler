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
        np_data = sampling_data_holder.get_np_data()
        mask_gb = np_data[:, SamplingRows.GB.value] == 1
        mask_kb = np_data[:, SamplingRows.KB.value] == 1
        mask_rb = np_data[:, SamplingRows.RB.value] == 1
        mask_ng = ~mask_gb & ~mask_kb & ~mask_rb
        self.precomputed_subsets: list[np.ndarray] = []
        for t in self.types:
            mask_type = np_data[:, SamplingRows.TYPE.value] == t
            for group_mask in (mask_gb, mask_kb, mask_rb, mask_ng):
                indices = np.where(mask_type & group_mask)[0]
                if len(indices) >= 2:
                    self.precomputed_subsets.append(indices)

    def evaluate(self, candidate):
        dates = candidate[:, SamplingRows.DATE.value]
        result = 1.0
        for indices in self.precomputed_subsets:
            result *= generate_score_np(dates[indices])
        return result

    def get_name(self) -> str:
        return "TypeSpreadEvaluator"
