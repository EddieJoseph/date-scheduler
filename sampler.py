from abc import abstractmethod
from datetime import datetime


class Sampler:
    @abstractmethod
    def sample(self, date: datetime.date) -> datetime.date:
        pass