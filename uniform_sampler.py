import datetime

import numpy as np

from sampler import Sampler


class UniformSampler(Sampler):
    def __init__(self, min=datetime.date.min, max=datetime.date.max):
        self.min = min
        self.max = max
        self.date_delta = (self.max - self.min + datetime.timedelta(days=1)).days
        # print(self.date_delta)

    def sample(self, date):
        # days between min and max
        #delta = self.max - self.min
        #print (delta)
        # random number between 0 and delta
        random_days = np.random.randint(self.date_delta)
        return self.min + datetime.timedelta(days=random_days)

