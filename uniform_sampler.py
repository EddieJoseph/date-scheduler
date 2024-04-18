import datetime

import numpy as np

from sampler import Sampler


class UniformSampler(Sampler):
    def __init__(self):
        self.date_delta = 365

    def sample(self, date):
        return (date + np.random.randint(self.date_delta))%365

