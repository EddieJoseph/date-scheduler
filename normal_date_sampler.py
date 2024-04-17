import datetime
import numpy as np

from sampler import Sampler


class NormalDateSampler(Sampler):

    def __init__(self, mean=0, variance=1, min=None, max=None):
        self.mean = mean
        self.variance = variance
        self.generator = np.random.normal(self.mean, self.variance)
        self.min = min
        self.max = max

    def sample(self,date):
        new_date = date + datetime.timedelta(days=round(np.random.normal(self.mean, self.variance),0))
        # check if new_date is between min and max
        if self.min is not None:
            if  new_date < self.min:
                new_date = self.sample(date)
                #new_date = self.min
        if self.max is not None:
            if  new_date > self.max:
                new_date = self.sample(date)
                #new_date = self.max

        return new_date

