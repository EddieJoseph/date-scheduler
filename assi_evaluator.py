import numpy as np
import pandas as pd

from evaluator import Evaluator


class AssiEvaluator(Evaluator):

    def evaluate(self, candidate):
        assi_dates = candidate[(candidate['type']=="ASI") | (candidate['type']=="ASIKVK")]
        diffs = assi_dates['order'].diff()
        violations = len(diffs[diffs < 0])
        return 0.5 ** violations

