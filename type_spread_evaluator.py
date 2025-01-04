import numpy as np

from evaluator import Evaluator
from row_names import RowNames


# def generate_score_n(indexes1, indexes2, dates):
#     comb_ind = np.intersect1d(indexes1, indexes2)
#     if len(comb_ind) < 2:
#         return 1
#     mask = np.isin(dates[:, 0], comb_ind)
#     dates_filtered = dates[mask, 1]
#     diffs = np.diff(dates_filtered)
#     diffs = np.append(diffs, 365 - dates_filtered[-1] + dates_filtered[0])
#     result = (1 / (1 + np.sqrt(np.var(diffs) / 10000)))
#     return result

def generate_score_n(indexes1, indexes2, dates):
    comb_ind = np.intersect1d(indexes1, indexes2)
    if len(comb_ind) < 2:
        return 1
    mask = np.isin(dates[:, 0], comb_ind)
    dates_filtered = dates[mask, 1]
    diffs = np.diff(dates_filtered, append=dates_filtered[0] + 365)
    result = 1 / (1 + np.sqrt(np.var(diffs) / 10000))
    return result

class TypeSpreadEvaluator(Evaluator):
    excluded_types = ["ST", "WTA", "SAN", "HY", "B", "ASSITST", "IFA", "MS", "KS"]
    types = []

    def evaluate(self, candidate):
        if len(self.types) == 0:
            self.types = super().get_types(candidate)
            self.types = [type for type in self.types if type not in self.excluded_types]
        result = 1
        # gb = candidate[candidate[RowNames.GB.value]][RowNames.GB.value].index.to_numpy()
        # kb = candidate[candidate[RowNames.KB.value]][RowNames.KB.value].index.to_numpy()
        # rb = candidate[candidate[RowNames.RB.value]][RowNames.RB.value].index.to_numpy()
        # ng = candidate[~candidate[RowNames.GB.value] & ~candidate[RowNames.KB.value] & ~candidate[
        #     RowNames.RB.value]].index.to_numpy()
        #
        # candidate[RowNames.DATE.value].to_numpy()
        # candidate[RowNames.DATE.value].index.to_numpy()
        # dates = np.column_stack(
        #     (candidate[RowNames.DATE.value].index.to_numpy(), candidate[RowNames.DATE.value].to_numpy()))

        gb = candidate.loc[candidate[RowNames.GB.value], RowNames.GB.value].index.to_numpy()
        kb = candidate.loc[candidate[RowNames.KB.value], RowNames.KB.value].index.to_numpy()
        rb = candidate.loc[candidate[RowNames.RB.value], RowNames.RB.value].index.to_numpy()
        ng = candidate.loc[~candidate[RowNames.GB.value] & ~candidate[RowNames.KB.value] & ~candidate[
            RowNames.RB.value]].index.to_numpy()

        dates = candidate[RowNames.DATE.value].reset_index().to_numpy()

        type_indexes = {}
        for type in self.types:
            t = candidate[candidate[RowNames.TYPE.value] == type][RowNames.TYPE.value].index.to_numpy()
            type_indexes[type] = t

        for t in type_indexes:
            result *= (generate_score_n(type_indexes[t], gb, dates)
                       * generate_score_n(type_indexes[t], kb, dates)
                       * generate_score_n(type_indexes[t], rb, dates)
                       * generate_score_n(type_indexes[t], ng, dates))
        return result

    def get_name(self) -> str:
        return "TypeSpreadEvaluator"
