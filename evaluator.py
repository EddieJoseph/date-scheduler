from abc import abstractmethod

import pandas as pd


class Evaluator:
    @abstractmethod
    def evaluate(self, dates:pd.DataFrame) -> float:
        pass


    def get_types(self, dates:pd.DataFrame) -> pd.DataFrame:
        return dates['type'].unique()





