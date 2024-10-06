from date_utils import get_month_from_day_of_year
from evaluator import Evaluator
from row_names import RowNames


class MonthEvaluator(Evaluator):

    def evaluate(self, dates):
        filtered = dates[dates[RowNames.DATE.value].notna()]
        months = filtered[RowNames.DATE.value].map(lambda d: get_month_from_day_of_year(d))
        diff = filtered[RowNames.MONTH.value] - months
        violations = diff.abs().sum()

        return 0.85 ** violations