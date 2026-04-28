import numpy as np

from ej.scheduler.generation.sampling_data_holder import SamplingRows, change_date
from .sampler import Sampler


class UniformSampler(Sampler):
    def __init__(self):
        self.date_delta = 365

    def _sample_date(self, date: int) -> int:
        return int((date + np.random.randint(self.date_delta)) % 365)

    def sample(self, candidate: np.ndarray) -> tuple[np.ndarray, set[int]]:
        not_fixed = np.where(candidate[:, SamplingRows.FIXED.value] == 0)[0]
        if len(not_fixed) == 0:
            return candidate, set()
        idx = int(np.random.choice(not_fixed))
        new_candidate = candidate.copy()
        change_date(new_candidate, idx, self._sample_date(int(new_candidate[idx, SamplingRows.DATE.value])))
        return new_candidate, {idx}
