from abc import abstractmethod

import pandas as pd
from numpy import ndarray

from ej.scheduler.util.row_names import RowNames


class Evaluator:
    @abstractmethod
    def evaluate(self, dates: pd.DataFrame) -> float:
        pass

    @abstractmethod
    def evaluate_np(self, dates:ndarray) -> float:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def get_types(self, dates: pd.DataFrame) -> pd.DataFrame:
        return dates[RowNames.TYPE.value].unique()
