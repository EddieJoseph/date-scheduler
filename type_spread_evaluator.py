import numpy as np
import pandas as pd

from evaluator import Evaluator


class TypeSpreadEvaluator(Evaluator):

    def evaluate(self, candidate):
        types = super().get_types(candidate)
        result = 1
        variance = []

        for type in types:
            type_candidates = candidate[candidate['type'] == type]
            for comp in ['RB', 'KB', 'GB']:
                type_comp_candidates = type_candidates[type_candidates[comp.lower()] == True]
                if len(type_comp_candidates) > 1:
                    dates = type_comp_candidates['date']
                    days_between = dates.diff()
                    days_between = days_between.fillna(365-dates.values[-1]+dates.values[0], inplace=False)
                    variance.append(days_between.var())
            no_type_comp_candidates = type_candidates[(type_candidates['gb'] == False) &
                                                      (type_candidates['kb'] == False) &
                                                      (type_candidates['rb'] == False)]

            if len(no_type_comp_candidates) > 1:
                dates = no_type_comp_candidates['date']
                days_between = dates.diff()
                days_between = days_between.fillna(365 - dates.values[-1] + dates.values[0], inplace=False)
                variance.append(days_between.var())

        mean_var = pd.Series(variance).mean()
        return 1/np.log10(mean_var+10)
        # return result / (1 + mean_var)
