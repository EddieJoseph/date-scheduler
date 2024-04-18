import datetime
import numpy as np

from sampler import Sampler


class NormalDateSampler(Sampler):

    def __init__(self, mean=0, variance=1):
        self.mean = mean
        self.variance = variance

    def sample(self,date):
        return (date+round(np.random.normal(self.mean, self.variance),0))%365


