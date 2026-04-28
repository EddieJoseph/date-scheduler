import numpy as np

from .sampler import Sampler


class NoChangeDateSampler(Sampler):
    def sample(self, candidate: np.ndarray) -> tuple[np.ndarray, set[int]]:
        return candidate, set()
