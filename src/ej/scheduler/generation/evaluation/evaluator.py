from abc import abstractmethod

import pandas as pd
from numpy import ndarray

from ej.scheduler.util.row_names import RowNames


class Evaluator:

    @abstractmethod
    def evaluate(self, dates: ndarray) -> float:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def evaluate_incremental(self, candidate: ndarray, changed_indices: set[int], cache: dict[int, float]) -> tuple[float, dict[int, float]]:
        return self.evaluate(candidate), {}

    def get_types(self, dates: pd.DataFrame) -> pd.DataFrame:
        return dates[RowNames.TYPE.value].unique()
