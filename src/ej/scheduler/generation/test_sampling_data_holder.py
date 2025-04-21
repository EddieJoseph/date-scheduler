from unittest import TestCase

import numpy as np

from ej.scheduler.generation.sampling_data_holder import SamplingDataHolder, sort_np_data, switch_dates, change_date
from ej.scheduler.util.scheduler_config import SchedulerData


class TestSamplingDataHolder(TestCase):

    def test_get_id_for_value(self):
        s = SamplingDataHolder(SchedulerData.create_from('../../../../input/performance_test.xlsx'))
        id = s._get_id_for_value("A", "A")
        self.assertEqual(id, 0)
        id = s._get_id_for_value("B", "A")
        self.assertEqual(id, 1)
        id = s._get_id_for_value("B", "B")
        self.assertEqual(id, 0)
        id = s._get_id_for_value("B", "B")
        self.assertEqual(id, 0)
        id = s._get_id_for_value("A", "A")
        self.assertEqual(id, 0)
        id = s._get_id_for_value("A", "B")
        self.assertEqual(id, 1)
        id = s._get_id_for_value("C", "A")
        self.assertEqual(id, 2)
        id = s._get_id_for_value("A", "A")
        self.assertEqual(id, 0)

    def test_get_value_for_id(self):
        s = SamplingDataHolder(SchedulerData.create_from('../../../../input/performance_test.xlsx'))
        id = s._get_id_for_value("A", "A")
        self.assertEqual(id, 0)
        id = s._get_id_for_value("B", "A")
        self.assertEqual(id, 1)
        id = s._get_id_for_value("B", "B")
        self.assertEqual(id, 0)
        id = s._get_id_for_value("B", "B")
        self.assertEqual(id, 0)
        id = s._get_id_for_value("A", "A")
        self.assertEqual(id, 0)
        id = s._get_id_for_value("A", "B")
        self.assertEqual(id, 1)
        id = s._get_id_for_value("C", "A")
        self.assertEqual(id, 2)
        id = s._get_id_for_value("A", "A")
        self.assertEqual(id, 0)

        self.assertEqual(s._get_value_for_id(0, "A"), "A")
        self.assertEqual(s._get_value_for_id(1, "A"), "B")
        self.assertEqual(s._get_value_for_id(0, "B"), "B")
        self.assertEqual(s._get_value_for_id(2, "A"), "C")
        self.assertEqual(s._get_value_for_id(10, "A"), None)
        self.assertEqual(s._get_value_for_id(2, "D"), None)



    def test_get_data_frame(self):
        data = SchedulerData.create_from('../../../../input/performance_test.xlsx')
        s = SamplingDataHolder(data)
        s.get_np_data()


    def test_get_scheduler_data(self):
        data = SchedulerData.create_from('../../../../input/performance_test.xlsx')
        initial_df = data.dates.reset_index(drop=True)
        s = SamplingDataHolder(data)
        export_df = s.get_scheduler_data().dates.reset_index(drop=True)

        # Check if the two dataframes are identical
        self.assertTrue(initial_df.equals(export_df))

    def test_sort_np_data(self):
        initial =  np.array( [[7, 8, 3], [1, 2, 9], [4, 5, 6]])
        goal = np.array([[1, 2, 9], [4, 5, 6], [7, 8, 3]])
        sorted_data = sort_np_data(initial, 1)
        assert np.array_equal(sorted_data, goal), "Sorting failed"
        goal = np.array([[7, 8, 3], [4, 5, 6], [1, 2, 9]])
        sorted_data = sort_np_data(initial, 2)
        assert np.array_equal(sorted_data, goal), "Sorting failed"

    def test_switch_dates(self):
        initial = np.array( [[1, 1, 1], [2, 2, 2], [3, 3, 3]])
        goal = np.array([[1, 1, 1], [2, 3, 3], [3, 2, 2]])
        switched_data = switch_dates(initial, 1, 2)
        assert np.array_equal(switched_data, goal), "Switch failed"

        goal = np.array([[1, 2, 2], [2, 3, 3], [3, 1, 1]])
        switched_data = switch_dates(switched_data, 0, 2)
        assert np.array_equal(switched_data, goal), "Switch failed"

    def test_change_date(self):
        initial = np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]])
        goal = np.array([[4, 1, 1], [2, 2, 2], [3, 3, 3]])
        changed_date = change_date(initial, 0, 4)
        assert np.array_equal(changed_date, goal), "Switch failed"

        goal = np.array([[4, 1, 1], [2, 2, 2], [7, 3, 3]])
        changed_date = change_date(changed_date, 2, 7)
        assert np.array_equal(changed_date, goal), "Switch failed"
