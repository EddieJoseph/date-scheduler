import numpy as np
import pandas as pd
import pytest

from ej.scheduler.generation.sampling_data_holder import SamplingRows
from ej.scheduler.util.row_names import RowNames
from ej.scheduler.util.scheduler_config import SchedulerData


@pytest.fixture
def make_events():
    def _make(n, **kwargs):
        data = np.zeros((n, 16), dtype=np.int16)
        data[:, SamplingRows.ID.value] = np.arange(n, dtype=np.int16)
        data[:, SamplingRows.INCLUDE.value] = 1
        data[:, SamplingRows.MONTH.value] = -1
        data[:, SamplingRows.ORDER.value] = -1
        for name, values in kwargs.items():
            data[:, SamplingRows[name.upper()].value] = values
        return data
    return _make


@pytest.fixture
def make_scheduler_data():
    def _make(n=2, **kwargs):
        # Columns in the exact order _convert_to_dataframe emits them
        defaults = {
            RowNames.DATE.value: list(range(1, n + 1)),
            RowNames.NAME.value: [f"name-{i}" for i in range(n)],
            RowNames.TYPE.value: ["A"] * n,
            RowNames.AS.value: [False] * n,
            RowNames.RB.value: [False] * n,
            RowNames.KB.value: [False] * n,
            RowNames.GB.value: [False] * n,
            RowNames.MOT.value: [False] * n,
            RowNames.ASI.value: [False] * n,
            RowNames.KADER.value: [False] * n,
            RowNames.OFF.value: [False] * n,
            RowNames.SAT.value: [False] * n,
            RowNames.MONTH.value: [np.nan] * n,
            RowNames.FIXED.value: [False] * n,
            RowNames.ORDER.value: [np.nan] * n,
            RowNames.TIME.value: [""] * n,
            RowNames.THEME.value: [""] * n,
            RowNames.CALLED_UP.value: [""] * n,
            RowNames.RESPONSIBLE.value: [""] * n,
            RowNames.DETAILS.value: [""] * n,
            RowNames.INCLUDE.value: [False] * n,
            RowNames.ID.value: [f"event-{i}" for i in range(n)],
        }
        defaults.update(kwargs)
        df = pd.DataFrame(defaults).reset_index(drop=True)
        df[RowNames.DATE.value] = df[RowNames.DATE.value].astype(np.int64)
        return SchedulerData(df, 0.0)
    return _make
