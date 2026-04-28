from datetime import datetime

import numpy as np
from numpy import ndarray

from .evaluator import Evaluator
from ..sampling_data_holder import SamplingDataHolder, SamplingRows


class WeekDayEvaluator(Evaluator):

    def __init__(self, year: int):
        self.year = year
        first_day = datetime(year, 1, 1)
        self.offset = first_day.weekday()
        self.types = []
        self.precomputed_subsets: list[np.ndarray] = []

    def add_type(self, type_name: str, sampling_data_holder: SamplingDataHolder):
        type_id = sampling_data_holder.map_types([type_name])[0]
        self.types.append(type_id)
        np_data = sampling_data_holder.get_np_data()
        type_mask = np_data[:, SamplingRows.TYPE.value] == type_id
        for group_col in (SamplingRows.RB.value, SamplingRows.KB.value, SamplingRows.GB.value):
            indices = np.where(type_mask & (np_data[:, group_col] == 1))[0]
            if len(indices) >= 1:
                self.precomputed_subsets.append(indices)

    def get_week_day(self, day):
        return (day + self.offset) % 7

    def evaluate_type_indexed(self, date_values: ndarray) -> float:
        weekdays = (date_values + self.offset) % 7
        filtered_weekdays = weekdays[weekdays < 4]
        if len(filtered_weekdays) < 1:
            return 1.0
        weekday_count = np.bincount(filtered_weekdays, minlength=4)
        a, b, c, d = weekday_count
        m = (a + b + c + d) * 0.25
        var = ((a - m)**2 + (b - m)**2 + (c - m)**2 + (d - m)**2) * 0.25
        result = 1 / (1 + np.sqrt(var / 10))
        return result

    def evaluate(self, dates: ndarray) -> float:
        date_col = dates[:, SamplingRows.DATE.value]
        result = 1.0
        for indices in self.precomputed_subsets:
            result *= self.evaluate_type_indexed(date_col[indices])
        return result

    def evaluate_incremental(self, candidate: ndarray, changed_indices: set[int], cache: dict[int, float]) -> tuple[float, dict[int, float]]:
        date_col = candidate[:, SamplingRows.DATE.value]
        result = 1.0
        new_cache = {}
        for i, indices in enumerate(self.precomputed_subsets):
            if any(idx in changed_indices for idx in indices):
                score = self.evaluate_type_indexed(date_col[indices])
            elif i in cache:
                score = cache[i]
            else:
                score = self.evaluate_type_indexed(date_col[indices])
            new_cache[i] = score
            result *= score
        return result, new_cache

    def get_name(self) -> str:
        return "WeekDayEvaluator"
