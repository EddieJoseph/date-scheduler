import numpy as np
import pandas as pd

from evaluator import Evaluator


class TypeSpreadEvaluator(Evaluator):

    def evaluate(self, candidate):
        types = super().get_types(candidate)
        excluded_types =["ST","WTA","SAN","HY","B","ASSITST","IFA","MS","KS"]
        types = [type for type in types if type not in excluded_types]
        result = 1

        for type in types:
            type_candidates = candidate[candidate['type'] == type]
            for comp in ['RB', 'KB', 'GB']:
                type_comp_candidates = type_candidates[type_candidates[comp.lower()] == True]
                if len(type_comp_candidates) > 1:
                    dates = type_comp_candidates['date']
                    days_between = dates.diff()
                    days_between = days_between.fillna(365-dates.values[-1]+dates.values[0], inplace=False)
                    result = result * (1/(1+np.sqrt(days_between.var()/10000)))
            no_type_comp_candidates = type_candidates[(type_candidates['gb'] == False) &
                                                      (type_candidates['kb'] == False) &
                                                      (type_candidates['rb'] == False)]

            if len(no_type_comp_candidates) > 1:
                dates = no_type_comp_candidates['date']
                days_between = dates.diff()
                days_between = days_between.fillna(365 - dates.values[-1] + dates.values[0], inplace=False)
                result = result * (1 / (1 + np.sqrt(days_between.var() / 10000)))
        return result

