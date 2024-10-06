from evaluator import Evaluator
from row_names import RowNames


class SameDayEvaluator(Evaluator):

    def evaluate(self, dates):
        # Evaluate the model on the same day data

        ex_per_day = dates[RowNames.DATE.value].value_counts()
        ex_per_day_c = len(ex_per_day[ex_per_day > 1])
        return 0.3 ** ex_per_day_c
