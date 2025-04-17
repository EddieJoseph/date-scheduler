from abc import abstractmethod


class Sampler:
    @abstractmethod
    def sample(self, date: int) -> int:
        pass
