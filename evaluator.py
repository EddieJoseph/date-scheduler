from abc import abstractmethod

import pandas as pd

from row_names import RowNames


class Evaluator:
    @abstractmethod
    def evaluate(self, dates:pd.DataFrame) -> float:
        pass


    def get_types(self, dates:pd.DataFrame) -> pd.DataFrame:
        return dates[RowNames.TYPE.value].unique()





