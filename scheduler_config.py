import pandas as pd
from pandas import DataFrame

from date_utils import convert_to_day_of_year, convert_to_datetime
from evaluator import Evaluator
from row_names import RowNames
from sampler import Sampler


class SchedulerConfig:

    def __init__(self, groups: DataFrame, year: int, evaluators: [Evaluator], sampler: Sampler):
        self.groups = groups
        self.year = year
        self.evaluators = evaluators
        self.sampler = sampler

    @staticmethod
    def create_from(path: str, year: int, evaluators: [Evaluator], sampler: Sampler):
        groups = pd.read_excel(path)
        return SchedulerConfig(groups, year, evaluators, sampler)


class SchedulerData:
    def __init__(self, dates: DataFrame, score: float):
        self.score = score
        self.dates = dates

    @staticmethod
    def create_from(path: str):
        dates = SchedulerData.load_dates(path)
        return SchedulerData(dates, 0.0)

    def save_to(self, year: int, path: str):
        SchedulerData.save_dates(self.dates, year, path)

    def clone(self):
        return SchedulerData(self.dates.copy(True), self.score)

    @staticmethod
    def load_dates(path: str):
        df = pd.read_excel(path)
        df[RowNames.DATE.value] = df[RowNames.DATE.value].map(lambda x: convert_to_day_of_year(x, throw_errors=False))
        df = df.sort_values(by=RowNames.DATE.value, inplace=False)
        return df

    @staticmethod
    def save_dates(dates: DataFrame, year: int, path: str):
        df = dates.copy(True)
        df[RowNames.DATE.value] = df[RowNames.DATE.value].map(lambda x: convert_to_datetime(x, year))
        df.to_excel(path, index=False)


def create_scheduler_config(dates_path: str, groups_path: str, year: int, evaluators: [Evaluator], sampler: Sampler):
    dates = pd.read_excel(dates_path)
    groups = pd.read_excel(groups_path)
    return SchedulerConfig(dates, groups, year, evaluators, sampler)


def create_new_scheduler_config(result: SchedulerData, config: SchedulerConfig):
    return SchedulerConfig(result.dates, config.groups, config.year, config.evaluators, config.sampler)


def clone_scheduler_config(config: SchedulerConfig):
    return SchedulerConfig(config.dates.copy(True), config.groups.copy(True), config.year, config.evaluators,
                           config.sampler)
