import numpy as np
import pandas as pd

from evaluator import Evaluator
from row_names import RowNames


class TypeSpreadEvaluator(Evaluator):

    def evaluate(self, candidate):
        types = super().get_types(candidate)
        excluded_types =["ST","WTA","SAN","HY","B","ASSITST","IFA","MS","KS"]
        types = [type for type in types if type not in excluded_types]
        result = 1

        for type in types:
            type_candidates = candidate[candidate[RowNames.TYPE.value] == type]
            for comp in [RowNames.RB.value, RowNames.KB.value, RowNames.GB.value]:
                type_comp_candidates = type_candidates[type_candidates[comp.lower()] == True]
                if len(type_comp_candidates) > 1:
                    dates = type_comp_candidates[RowNames.DATE.value]
                    days_between = dates.diff()
                    days_between = days_between.fillna(365-dates.values[-1]+dates.values[0], inplace=False)
                    result = result * (1/(1+np.sqrt(days_between.var()/10000)))
            no_type_comp_candidates = type_candidates[(type_candidates[RowNames.GB.value] == False) &
                                                      (type_candidates[RowNames.KB.value] == False) &
                                                      (type_candidates[RowNames.RB.value] == False)]

            if len(no_type_comp_candidates) > 1:
                dates = no_type_comp_candidates[RowNames.DATE.value]
                days_between = dates.diff()
                days_between = days_between.fillna(365 - dates.values[-1] + dates.values[0], inplace=False)
                result = result * (1 / (1 + np.sqrt(days_between.var() / 10000)))
        return result

