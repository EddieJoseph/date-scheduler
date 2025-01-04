import numpy as np
import pandas as pd

from evaluator import Evaluator
from row_names import RowNames
from joblib import Parallel, delayed


def generate_score_n(indexes1, indexes2, dates):
    comb_ind = np.intersect1d(indexes1, indexes2)

    if len(comb_ind) < 2:
        return 1

    mask = np.isin(dates[:, 0], comb_ind)
    dates_filtered = dates[mask, 1]

    diffs = np.diff(dates_filtered)
    diffs = np.append(diffs, 365 - dates_filtered[-1] + dates_filtered[0])

    result = (1 / (1 + np.sqrt(np.var(diffs) / 10000)))
    return result


class TypeSpreadEvaluator(Evaluator):
    excluded_types = ["ST", "WTA", "SAN", "HY", "B", "ASSITST", "IFA", "MS", "KS"]
    types = []
    # 80% time
    # def evaluate(self, candidate):
    #     if len(self.types) == 0:
    #         self.types = super().get_types(candidate)
    #         self.types = [type for type in self.types if type not in self.excluded_types]
    #     result = 1
    #
    #     for comp in [RowNames.RB.value, RowNames.KB.value, RowNames.GB.value]:
    #         comp_candidates = candidate[candidate[comp.lower()] == True]
    #         for type in self.types:
    #             type_comp_candidates = comp_candidates[comp_candidates[RowNames.TYPE.value] == type]
    #             if len(type_comp_candidates) > 1:
    #                 result = result * self.generate_score(type_comp_candidates)
    #     no_type_candidates = candidate[(candidate[RowNames.GB.value] == False) &
    #                                     (candidate[RowNames.KB.value] == False) &
    #                                     (candidate[RowNames.RB.value] == False)]
    #     for type in self.types:
    #         no_type_comp_candidates = no_type_candidates[no_type_candidates[RowNames.TYPE.value] == type]
    #         if len(no_type_comp_candidates) > 1:
    #             result = result * self.generate_score(no_type_comp_candidates)
    #     return result

    def evaluate(self, candidate):
        if len(self.types) == 0:
            self.types = super().get_types(candidate)
            self.types = [type for type in self.types if type not in self.excluded_types]
        result = 1
        gb = candidate[candidate[RowNames.GB.value]][RowNames.GB.value].index.to_numpy()
        kb = candidate[candidate[RowNames.KB.value]][RowNames.KB.value].index.to_numpy()
        rb = candidate[candidate[RowNames.RB.value]][RowNames.RB.value].index.to_numpy()
        ng = candidate[~candidate[RowNames.GB.value] & ~candidate[RowNames.KB.value] & ~candidate[RowNames.RB.value]].index.to_numpy()

        candidate[RowNames.DATE.value].to_numpy()
        candidate[RowNames.DATE.value].index.to_numpy()
        dates = np.column_stack((candidate[RowNames.DATE.value].index.to_numpy(), candidate[RowNames.DATE.value].to_numpy()))

        type_indexes = {}
        for type in self.types:
            t = candidate[candidate[RowNames.TYPE.value] == type][RowNames.TYPE.value].index.to_numpy()
            type_indexes[type] = t

        for t in type_indexes:
            result *= generate_score_n(type_indexes[t], gb, dates)
            result *= generate_score_n(type_indexes[t], kb, dates)
            result *= generate_score_n(type_indexes[t], rb, dates)
            result *= generate_score_n(type_indexes[t], ng, dates)

        return result

    # #66% time
    # def evaluate(self, candidate):
    #     # Initialize result
    #     result = 1
    #
    #     # Compute self.types if not already done
    #     if not self.types:
    #         all_types = super().get_types(candidate)
    #         self.types = [type for type in all_types if type not in self.excluded_types]
    #
    #     # Separate candidates with and without component flags
    #     type_candidates = candidate[
    #         candidate[[RowNames.RB.value, RowNames.KB.value, RowNames.GB.value]].any(axis=1)
    #     ]
    #     no_type_candidates = candidate[
    #         ~candidate[[RowNames.RB.value, RowNames.KB.value, RowNames.GB.value]].any(axis=1)
    #     ]
    #
    #     # Process candidates with component flags
    #     if not type_candidates.empty:
    #         for comp in [RowNames.RB.value, RowNames.KB.value, RowNames.GB.value]:
    #             comp_candidates = type_candidates[type_candidates[comp.lower()]]
    #             if not comp_candidates.empty:
    #                 grouped = comp_candidates.groupby(RowNames.TYPE.value)
    #                 for type, group in grouped:
    #                     if type in self.types and len(group) > 1:
    #                         result *= self.generate_score(group)
    #
    #     # Process candidates without any component flags
    #     if not no_type_candidates.empty:
    #         grouped = no_type_candidates.groupby(RowNames.TYPE.value)
    #         for type, group in grouped:
    #             if type in self.types and len(group) > 1:
    #                 result *= self.generate_score(group)
    #
    #     return result

    # #50% time but not correct
    # def evaluate(self, candidate):
    #     if len(self.types) == 0:
    #         all_types = super().get_types(candidate)
    #         self.types = np.array([type for type in all_types if type not in self.excluded_types])
    #
    #     # Convert relevant columns to NumPy arrays for speed
    #     type_col = candidate[RowNames.TYPE.value].values
    #     comp_flags = candidate[[RowNames.RB.value, RowNames.KB.value, RowNames.GB.value]].values
    #     has_comp_flags = comp_flags.any(axis=1)
    #     type_candidates = candidate[has_comp_flags]
    #     no_type_candidates = candidate[~has_comp_flags]
    #
    #     def process_group(type_data, comp_flags_subset):
    #         result = 1
    #         unique_types = np.intersect1d(type_data, self.types)
    #         for type in unique_types:
    #             indices = np.where(type_data == type)[0]
    #             if len(indices) > 1:
    #                 result *= self.generate_score(type_candidates.iloc[indices])
    #         return result
    #
    #     # # Process candidates with component flags
    #     # result_with_flags = Parallel(n_jobs=-1)(
    #     #     delayed(process_group)(
    #     #         type_candidates[RowNames.TYPE.value].values,
    #     #         comp_flags
    #     #     )
    #     # )
    #     result_with_flags = process_group(type_candidates[RowNames.TYPE.value].values,comp_flags)
    #
    #
    #     # # Process candidates without component flags
    #     # result_no_flags = Parallel(n_jobs=-1)(
    #     #     delayed(process_group)(
    #     #         no_type_candidates[RowNames.TYPE.value].values,
    #     #         np.zeros_like(comp_flags)
    #     #     )
    #     # )
    #     result_no_flags = process_group(no_type_candidates[RowNames.TYPE.value].values, np.zeros_like(comp_flags))
    #
    #     # Combine results
    #     result = np.prod(result_with_flags) * np.prod(result_no_flags)
    #     return result
    def generate_score(self, type_comp_candidates):
        dates = type_comp_candidates[RowNames.DATE.value]
        days_between = dates.diff()
        days_between.fillna(365 - dates.values[-1] + dates.values[0], inplace=True)
        result = (1 / (1 + np.sqrt(days_between.var() / 10000)))
        return result

    def get_name(self) -> str:
        return "TypeSpreadEvaluator"