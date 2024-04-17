import numpy as np
import pandas as pd

from evaluator import Evaluator
from sampler import Sampler


class DateScheduler:

    def __init__(self):
        self.evaluators = []

    def load_people(self, path: str):
        self.groups = pd.read_excel(path)
        pass

    def get_groups(self):
        return self.groups

    def load_dates(self, path: str):
        self.initial_dates = pd.read_excel(path)
        self.dates = self.initial_dates.sort_values(by='date', inplace=False)

    def save_dates(self, path: str):
        self.dates.to_excel(path, index=False)

    def set_sampler(self, sampler: Sampler):
        self.sampler = sampler

    def add_evaluator(self, evaluator: Evaluator):
        self.evaluators.append(evaluator)

    def initialize(self, sampler: Sampler):
        for index, row in self.dates.iterrows():
            self.dates.loc[index, 'date'] = sampler.sample(row['date'].date())
        self.dates.sort_values(by='date', inplace=True)

    def generate_candidate(self):
        candidate = self.dates.copy()
        for index, row in candidate.iterrows():
            candidate.loc[index, 'date'] = self.sampler.sample(row['date'])
        # sort candidate by date ascending
        return candidate.sort_values(by='date', inplace=False)
        # return candidate

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
            # if new_p > initial_p:
            #     self.dates = cand
            #     initial_p = new_p
            #     # print("improved")
            # else:
            #     if np.random.rand() < new_p / initial_p:
            #         self.dates = cand
            #         initial_p = new_p
            #         # print("deradign step accepted")
            #     else:
            #         # print("degrading step rejected")
            #         pass


            if min(1,new_p / initial_p) > np.random.rand()**0.05:
                self.dates = cand
                initial_p = new_p
                accept += 1
            else:
                reject += 1


        print(initial_p,";", accept / (accept + reject))
        return initial_p

    def iterate_until(self, iterations=1, threshold=0.9):
        initial_p = self.evaluate_candidate(self.dates)
        while initial_p < threshold:
            initial_p= self.iterate(iterations)
        return initial_p

    def get_result(self):
        return self.dates