from abc import abstractmethod

import numpy as np


class Sampler:
    @abstractmethod
    def sample(self, candidate: np.ndarray) -> tuple[np.ndarray, set[int]]:
        pass
