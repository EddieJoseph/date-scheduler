import pandas as pd

from ej.scheduler.util.date_utils import convert_to_day_of_year
from ej.scheduler.util.row_names import RowNames, HolidayRowNames
from .evaluator import Evaluator


class JfHolidayEvaluator(Evaluator):

    def __init__(self, path: str):
        holidays = pd.read_excel(path)

        self.blocked_dates = []

        for index, row in holidays.iterrows():
            if row[HolidayRowNames.ONLY_JF.value]:
                start = convert_to_day_of_year(row[HolidayRowNames.START.value])
                end = convert_to_day_of_year(row[HolidayRowNames.END.value]) + 1
                for d in range(start, end):
                    self.blocked_dates.append(d)

    def evaluate(self, dates: pd.DataFrame) -> float:
        filtered_dates = dates[dates[RowNames.TYPE.value] == 'J']
        return 0.8 ** len(filtered_dates[(filtered_dates[RowNames.DATE.value].isin(self.blocked_dates))])

    def get_name(self) -> str:
        return "JfHolidayEvaluator"
