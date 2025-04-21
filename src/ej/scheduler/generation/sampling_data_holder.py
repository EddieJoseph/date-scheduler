from enum import Enum

import numpy as np
import pandas as pd

from ej.scheduler.util.row_names import RowNames
from ej.scheduler.util.scheduler_config import SchedulerData


class SamplingRows(Enum):
    DATE = 0
    MONTH = 1
    TYPE = 2
    AS = 3
    KB = 4
    GB = 5
    RB = 6
    MOT = 7
    ASI = 8
    KADER = 9
    OFF = 10
    SAT = 11
    FIXED = 12
    ID = 13
    ORDER = 14
    INCLUDE = 15

def sort_np_data(np_data: np.ndarray, column_to_sort_by: int):
    sorted_indices = np.argsort(np_data[:, column_to_sort_by])
    sorted_array = np_data[sorted_indices, :]
    return sorted_array

def switch_dates(np_data: np.ndarray, index1: int, index2: int):
    temp = np.copy(np_data[index1,:])
    temp[SamplingRows.DATE.value] = np_data[index2, SamplingRows.DATE.value]
    np_data[index1,:] = [np_data[index1, SamplingRows.DATE.value], *np_data[index2, SamplingRows.DATE.value + 1:]]
    np_data[index2, :] = temp
    return np_data

def change_date(np_data: np.ndarray, index: int, new_date: int):
    np_data[index, SamplingRows.DATE.value] = new_date
    return np_data

class SamplingDataHolder:

    def __init__(self, data: SchedulerData):
        self.data = data
        self.mapping = {}
        self.current_ids = {}
        self.np_data = self._convert_from_dataframe(self.data.dates)
        self.score = self.data.score

        self.types = self.data.dates[RowNames.TYPE.value].unique()

    def get_scheduler_data(self) -> SchedulerData:
        self.data.dates = self._convert_to_dataframe()
        self.data.score = self.score
        return self.data

    def get_types(self):
        return self.types

    def get_np_data(self) -> np.ndarray:
        return self.np_data

    def set_np_data(self, np_data: np.ndarray):
        self.np_data = np_data

    def get_score(self) -> float:
        return self.score

    def set_score(self, score: float):
        self.score = score

    def _convert_from_dataframe(self, data_frame):
        np_data = np.ones((len(data_frame), 16), dtype=np.int16) * -1
        print(np_data)
        for index, row in data_frame.iterrows():
            np_data[index, SamplingRows.DATE.value] = row[RowNames.DATE.value]
            if not np.isnan(row[RowNames.MONTH.value]):
                np_data[index, SamplingRows.MONTH.value] = row[RowNames.MONTH.value]
            np_data[index, SamplingRows.TYPE.value] = self._get_id_for_value(row[RowNames.TYPE.value], RowNames.TYPE.value)
            np_data[index, SamplingRows.AS.value] = 1 if row[RowNames.AS.value] else 0
            np_data[index, SamplingRows.KB.value] = 1 if row[RowNames.KB.value] else 0
            np_data[index, SamplingRows.GB.value] = 1 if row[RowNames.GB.value] else 0
            np_data[index, SamplingRows.RB.value] = 1 if row[RowNames.RB.value] else 0
            np_data[index, SamplingRows.MOT.value] = 1 if row[RowNames.MOT.value] else 0
            np_data[index, SamplingRows.ASI.value] = 1 if row[RowNames.ASI.value] else 0
            np_data[index, SamplingRows.KADER.value] = 1 if row[RowNames.KADER.value] else 0
            np_data[index, SamplingRows.OFF.value] = 1 if row[RowNames.OFF.value] else 0
            np_data[index, SamplingRows.SAT.value] = 1 if row[RowNames.SAT.value] else 0
            np_data[index, SamplingRows.FIXED.value] = 1 if row[RowNames.FIXED.value] else 0
            np_data[index, SamplingRows.ID.value] = self._get_id_for_value(row[RowNames.ID.value], RowNames.ID.value)
            if not np.isnan(row[RowNames.ORDER.value]):
                np_data[index, SamplingRows.ORDER.value] = row[RowNames.ORDER.value]
            np_data[index, SamplingRows.INCLUDE.value] = 1 if row[RowNames.INCLUDE.value] else 0

        return np_data

    def _get_values_based_on_id(self, ids: np.ndarray, row):
        ret = []
        for id in ids:
            translated_id = self._get_value_for_id(id, RowNames.ID.value)
            id_row = self.data.dates[self.data.dates[RowNames.ID.value] == translated_id]
            ret.append(id_row[row].iloc[0])
        return ret

    def _convert_to_dataframe(self):
        sorted_np_data = sort_np_data(self.np_data, SamplingRows.DATE.value)
        data_frame = pd.DataFrame()
        data_frame[RowNames.DATE.value] = sorted_np_data[:, SamplingRows.DATE.value].astype(dtype=np.int64)
        data_frame[RowNames.NAME.value] = self._get_values_based_on_id(sorted_np_data[:, SamplingRows.ID.value],
                                                                       RowNames.NAME.value)
        data_frame[RowNames.TYPE.value] = [self._get_value_for_id(x, RowNames.TYPE.value) for x in
                                           sorted_np_data[:, SamplingRows.TYPE.value]]
        data_frame[RowNames.AS.value] = [x == 1 for x in sorted_np_data[:, SamplingRows.AS.value]]
        data_frame[RowNames.RB.value] = [x == 1 for x in sorted_np_data[:, SamplingRows.RB.value]]
        data_frame[RowNames.KB.value] = [x == 1 for x in sorted_np_data[:, SamplingRows.KB.value]]
        data_frame[RowNames.GB.value] = [x == 1 for x in sorted_np_data[:, SamplingRows.GB.value]]
        data_frame[RowNames.MOT.value] = [x == 1 for x in sorted_np_data[:, SamplingRows.MOT.value]]
        data_frame[RowNames.ASI.value] = [x == 1 for x in sorted_np_data[:, SamplingRows.ASI.value]]
        data_frame[RowNames.KADER.value] = [x == 1 for x in sorted_np_data[:, SamplingRows.KADER.value]]
        data_frame[RowNames.OFF.value] = [x == 1 for x in sorted_np_data[:, SamplingRows.OFF.value]]
        data_frame[RowNames.SAT.value] = [x == 1 for x in sorted_np_data[:, SamplingRows.SAT.value]]
        data_frame[RowNames.MONTH.value] = data_frame[RowNames.MONTH.value] = np.where(
            sorted_np_data[:, SamplingRows.MONTH.value] == -1, np.nan, sorted_np_data[:, SamplingRows.MONTH.value])
        data_frame[RowNames.FIXED.value] = [x == 1 for x in sorted_np_data[:, SamplingRows.FIXED.value]]
        data_frame[RowNames.ORDER.value] = np.where(sorted_np_data[:, SamplingRows.ORDER.value] == -1, np.nan,
                                                    sorted_np_data[:, SamplingRows.ORDER.value])
        data_frame[RowNames.TIME.value] = self._get_values_based_on_id(sorted_np_data[:, SamplingRows.ID.value],
                                                                       RowNames.TIME.value)
        data_frame[RowNames.THEME.value] = self._get_values_based_on_id(sorted_np_data[:, SamplingRows.ID.value],
                                                                        RowNames.THEME.value)
        data_frame[RowNames.CALLED_UP.value] = self._get_values_based_on_id(sorted_np_data[:, SamplingRows.ID.value],
                                                                            RowNames.CALLED_UP.value)
        data_frame[RowNames.RESPONSIBLE.value] = self._get_values_based_on_id(sorted_np_data[:, SamplingRows.ID.value],
                                                                              RowNames.RESPONSIBLE.value)
        data_frame[RowNames.DETAILS.value] = self._get_values_based_on_id(sorted_np_data[:, SamplingRows.ID.value],
                                                                          RowNames.DETAILS.value)
        data_frame[RowNames.INCLUDE.value] = [x == 1 for x in sorted_np_data[:, SamplingRows.INCLUDE.value]]
        data_frame[RowNames.ID.value] = [self._get_value_for_id(x, RowNames.ID.value) for x in
                                         sorted_np_data[:, SamplingRows.ID.value]]
        return data_frame

    def _get_id_for_value(self, value, value_type: str):
        if value_type not in self.mapping:
            self.mapping[value_type] = {}
            self.current_ids[value_type] = 0

        if value not in self.mapping[value_type]:
            self.mapping[value_type][value] = self.current_ids[value_type]
            self.current_ids[value_type] += 1

        return self.mapping[value_type][value]

    def _get_value_for_id(self, id: int, value_type: str):
        if value_type not in self.mapping:
            return None

        for key, value in self.mapping[value_type].items():
            if value == id:
                return key
        return None
