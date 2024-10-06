import pandas as pd

from date_utils import convert_to_day_of_year
from evaluator import Evaluator
from row_names import RowNames, HolidayRowNames


class HolidayEvaluator(Evaluator):

    def __init__(self, path: str):
        holidays = pd.read_excel(path)

        self.blocked_dates = []

        for index, row in holidays.iterrows():
            if not row[HolidayRowNames.ONLY_JF.value]:
                start = convert_to_day_of_year(row[HolidayRowNames.START.value])
                end = convert_to_day_of_year(row[HolidayRowNames.END.value]) + 1
                for d in range(start, end):
                    self.blocked_dates.append(d)

    def evaluate(self, dates: pd.DataFrame) -> float:
        return 0.8 ** len(dates[(dates[RowNames.FIXED.value].isin(self.blocked_dates))])
