import pandas as pd

from date_utils import convert_to_day_of_year
from evaluator import Evaluator


class JfHolidayEvaluator(Evaluator):

    def __init__(self, path: str):
        holidays = pd.read_excel(path)

        self.blocked_dates = []

        for index, row in holidays.iterrows():
            if row['only_jf']:
                start = convert_to_day_of_year(row['start'])
                end = convert_to_day_of_year(row['end']) + 1
                for d in range(start, end):
                    self.blocked_dates.append(d)

    def evaluate(self, dates: pd.DataFrame) -> float:
        filtered_dates = dates[dates['type'] == 'J']
        return 0.8 ** len(filtered_dates[(filtered_dates['date'].isin(self.blocked_dates))])
