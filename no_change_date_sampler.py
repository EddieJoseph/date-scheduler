from datetime import datetime

from sampler import Sampler


class NoChangeDateSampler(Sampler):
    def sample(self, date: datetime.date) -> datetime.date:
        return date