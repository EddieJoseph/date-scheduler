from date_utils import get_month_from_day_of_year
from evaluator import Evaluator


class MonthEvaluator(Evaluator):

    def evaluate(self, dates):
        # Evaluate the model on the same day data

        # violations = 3

        #filter dates to only include non nan months
        filtered = dates[dates['month'].notna()]

        months = filtered['date'].map(lambda d: get_month_from_day_of_year(d))
        diff = filtered['month'] - months
        violations = diff.abs().sum()



        return 0.95 ** violations