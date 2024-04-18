import pandas as pd

from date_utils import convert_to_day_of_year
from evaluator import Evaluator


class HolidayEvaluator(Evaluator):

    def __init__(self, path: str):
        holidays = pd.read_excel(path)

        self.blocked_dates = []
        self.blocked_values = []

        for index, row in holidays.iterrows():
            start = convert_to_day_of_year(row['start'])
            end = convert_to_day_of_year(row['end']) + 1
            for d in range(start, end):
                self.blocked_dates.append(d)
                self.blocked_values.append(row['importance'])

    def evaluate(self, dates: pd.DataFrame) -> float:
        return 0.8 ** len(dates[(dates['date'].isin(self.blocked_dates))])
        # return 0.8 ** len(dates[(dates['type'] != 'KP') & (dates['date'].isin(self.blocked_dates))])
