import numpy as np
import pandas as pd

from evaluator import Evaluator


class TypeSpreadEvaluator(Evaluator):

    def evaluate(self, candidate):
        types = super().get_types(candidate)
        result = 1
        # variance = []

        for type in types:
            type_candidates = candidate[candidate['type'] == type]
            for comp in ['RB', 'KB', 'GB']:
                type_comp_candidates = type_candidates[type_candidates[comp.lower()] == True]
                if len(type_comp_candidates) > 1:
                    dates = type_comp_candidates['date']
                    days_between = dates.diff()
                    days_between = days_between.fillna(365-dates.values[-1]+dates.values[0], inplace=False)
                    # variance.append(days_between.var())
                    result = result * (1/(1+np.sqrt(days_between.var()/10000)))
                    # print ("partial_result",(1/(1+np.sqrt(days_between.var()/10000))))
            no_type_comp_candidates = type_candidates[(type_candidates['gb'] == False) &
                                                      (type_candidates['kb'] == False) &
                                                      (type_candidates['rb'] == False)]

            if len(no_type_comp_candidates) > 1:
                dates = no_type_comp_candidates['date']
                days_between = dates.diff()
                days_between = days_between.fillna(365 - dates.values[-1] + dates.values[0], inplace=False)
                # variance.append(days_between.var())
                result = result * (1 / (1 + np.sqrt(days_between.var() / 10000)))

        # mean_var = pd.Series(variance).mean()
        # return 1/np.log10(mean_var+10)
        # print("result", result)
        return result

    def evaluate2(self, candidate):
        types = super().get_types(candidate)

        violations = np.array([])

        for type in types:
            type_candidates = candidate[candidate['type'] == type]
            for comp in ['RB', 'KB', 'GB']:
                type_comp_candidates = type_candidates[type_candidates[comp.lower()] == True]
                if len(type_comp_candidates) > 1:
                    dates = type_comp_candidates['date']
                    days_between = dates.diff()
                    days_between = days_between.fillna(365-dates.values[-1]+dates.values[0], inplace=False)
                    355/len(days_between)*1.5
                    violations = np.concatenate([violations, days_between[days_between > 355/len(days_between)*1.5]])




            no_type_comp_candidates = type_candidates[(type_candidates['gb'] == False) &
                                                      (type_candidates['kb'] == False) &
                                                      (type_candidates['rb'] == False)]

            if len(no_type_comp_candidates) > 1:
                dates = no_type_comp_candidates['date']
                days_between = dates.diff()
                days_between = days_between.fillna(365 - dates.values[-1] + dates.values[0], inplace=False)
                violations  = np.concatenate([violations, days_between[days_between > 355 / len(days_between) * 1.5]])


        result = 0.7**len(violations)
        return result
