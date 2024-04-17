import pandas as pd

from evaluator import Evaluator


class TypeSpreadEvaluator(Evaluator):
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def evaluate(self, candidate):
        types = super().get_types(candidate)

        result = 1
        variance = []

        for type in types:
            type_candidates = candidate[candidate['type'] == type]

            # get days between two dates
            dates = type_candidates['date']
            from_start = dates.values[0] - self.min
            to_end = self.max - dates.values[-1]
            days_between = dates.diff().dt.days

            # replace the nan value with 10
            days_between = days_between.fillna((from_start + to_end).days, inplace=False)

            # variance.append(days_between.var())
            variance.append(days_between.std())

        mean_var = pd.Series(variance).mean()
        # print(mean_var)
        return result / (1 + mean_var)
