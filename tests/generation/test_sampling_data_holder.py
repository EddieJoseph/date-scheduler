import numpy as np

from ej.scheduler.generation.sampling_data_holder import SamplingDataHolder, change_date, sort_np_data, switch_dates


def test_sort_np_data():
    data = np.array([[7, 8, 3], [1, 2, 9], [4, 5, 6]])
    assert np.array_equal(sort_np_data(data, 1), [[1, 2, 9], [4, 5, 6], [7, 8, 3]])
    assert np.array_equal(sort_np_data(data, 2), [[7, 8, 3], [4, 5, 6], [1, 2, 9]])


def test_switch_dates():
    data = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    result = switch_dates(data, 1, 2)
    assert np.array_equal(result, [[1, 1, 1], [2, 3, 3], [3, 2, 2]])


def test_change_date():
    data = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
    result = change_date(data, 0, 4)
    assert np.array_equal(result, [[4, 1, 1], [2, 2, 2], [3, 3, 3]])
    result = change_date(result, 2, 7)
    assert np.array_equal(result, [[4, 1, 1], [2, 2, 2], [7, 3, 3]])


def test_round_trip(make_scheduler_data):
    data = make_scheduler_data(2)
    initial_df = data.dates.reset_index(drop=True)
    s = SamplingDataHolder(data)
    export_df = s.get_scheduler_data().dates.reset_index(drop=True)
    assert initial_df.equals(export_df)
