import numpy as np

from sampler import Sampler


class CombinedSampler(Sampler):
    def __init__(self, samplers: [Sampler], weights: [float]):
        if len(samplers) != len(weights):
            raise ValueError("samplers and weights must have the same length")
        if sum(weights) != 1:
            weights = [w / sum(weights) for w in weights]

        self.weights = weights
        self.samplers = samplers

    def sample(self, date):
        sampler = np.random.choice(self.samplers, p=self.weights)
        return sampler.sample(date)
