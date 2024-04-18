import datetime
from functools import partial

import numpy as np
import pandas as pd

from date_utils import convert_to_day_of_year, convert_to_datetime
from evaluator import Evaluator
from sampler import Sampler


class DateScheduler:

    def __init__(self, year:int):
        self.evaluators = []
        self.year = year

    def load_people(self, path: str):
        self.groups = pd.read_excel(path)
        self.max_p=0
        self.max_dates = None

        pass

    def get_groups(self):
        return self.groups

    def load_dates(self, path: str):
        # date_parser = lambda x: pd.datetime.strptime(x, '%d.%m.%Y')
        # date_parser = partial(pd.to_datetime, format='%d.%m.%Y')
        # self.initial_dates = pd.read_excel(path)
        df = pd.read_excel(path)

        # map df['date'] to tay of year or random number
        df['date'] = df['date'].map(lambda x: convert_to_day_of_year(x, throw_errors=False))
        df = df.sort_values(by='date', inplace=False)

        self.initial_dates = df
        self.dates = df.copy(True)

    def save_dates(self, path: str):
        df = self.dates.copy(True)
        df['date'] = df['date'].map(lambda x: convert_to_datetime(x, self.year))
        df.to_excel(path, index=False)

    def set_sampler(self, sampler: Sampler):
        self.sampler = sampler

    def add_evaluator(self, evaluator: Evaluator):
        self.evaluators.append(evaluator)

    # def initialize(self, sampler: Sampler):
    #     for index, row in self.dates.iterrows():
    #         self.dates.loc[index, 'date'] = sampler.sample(row['date'])
    #     self.dates.sort_values(by='date', inplace=True)

    def generate_candidate2(self):
        candidate = self.dates.copy()
        for index, row in candidate.iterrows():
            candidate.loc[index, 'date'] = self.sampler.sample(row['date'])
        # sort candidate by date ascending
        return candidate.sort_values(by='date', inplace=False)
        # return candidate
    def generate_candidate(self):

        rows_to_change = np.random.randint(0, len(self.dates), np.random.randint(1, 4))
        candidate = self.dates.copy()
        if len(rows_to_change)==2 and np.random.randint(10) < 1:
            candidate.loc[rows_to_change[0], 'date'] = self.dates.loc[rows_to_change[1], 'date']
            candidate.loc[rows_to_change[1], 'date'] = self.dates.loc[rows_to_change[0], 'date']
        else:
            for index in rows_to_change:
                self.dates.loc[index, 'date'] = self.sampler.sample(self.dates.loc[index, 'date'])
        return candidate.sort_values(by='date', inplace=False)

    def evaluate_candidate(self, candidate):
        total = 1
        for evaluator in self.evaluators:
            total *= evaluator.evaluate(candidate)
        return total

    def iterate(self, iterations=1):
        initial_p = self.evaluate_candidate(self.dates)
        accept = 0
        reject = 0
        for i in range(iterations):
            cand = self.generate_candidate()
            new_p = self.evaluate_candidate(cand)

            if (initial_p > self.max_p):
                self.max_p = initial_p
                self.max_dates = self.dates.copy(True)

            if min(1, new_p / initial_p) > np.random.rand() ** 0.03:
                self.dates = cand
                initial_p = new_p
                accept += 1
            else:
                reject += 1

        print(initial_p, ";", accept / (accept + reject),";",self.max_p )

        # for i in range(iterations):
        #     cand = self.generate_candidate()
        #     new_p = self.evaluate_candidate(cand)
        #     if new_p > initial_p:
        #         self.dates = cand
        #         initial_p = new_p
        #     if (initial_p > self.max_p):
        #         self.max_p = initial_p
        #         self.max_dates = self.dates.copy(True)
        # print(initial_p)
        #
        # return initial_p

    def get_max(self):
        return self.max_p

    def save_max(self, path: str):
        df = self.max_dates.copy(True)
        df['date'] = df['date'].map(lambda x: convert_to_datetime(x, self.year))
        df.to_excel(path, index=False)

    def iterate_until(self, iterations=1, threshold=0.9):
        initial_p = self.evaluate_candidate(self.dates)
        while initial_p < threshold:
            initial_p = self.iterate(iterations)
        return initial_p

    def get_result(self):
        return self.dates
