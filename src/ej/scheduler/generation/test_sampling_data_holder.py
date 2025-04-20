from unittest import TestCase

import numpy as np

from ej.scheduler.generation.sampling_data_holder import SamplingDataHolder
from ej.scheduler.util.scheduler_config import SchedulerData


class TestSamplingDataHolder(TestCase):

    def test_get_id_for_value(self):
        s = SamplingDataHolder()
        id = s.get_id_for_value("A","A")
        self.assertEqual(id, 0)
        id = s.get_id_for_value("B", "A")
        self.assertEqual(id, 1)
        id = s.get_id_for_value("B", "B")
        self.assertEqual(id, 0)
        id = s.get_id_for_value("B", "B")
        self.assertEqual(id, 0)
        id = s.get_id_for_value("A", "A")
        self.assertEqual(id, 0)
        id = s.get_id_for_value("A", "B")
        self.assertEqual(id, 1)
        id = s.get_id_for_value("C", "A")
        self.assertEqual(id, 2)
        id = s.get_id_for_value("A", "A")
        self.assertEqual(id, 0)

    def test_get_value_for_id(self):
        s = SamplingDataHolder()
        id = s.get_id_for_value("A", "A")
        self.assertEqual(id, 0)
        id = s.get_id_for_value("B", "A")
        self.assertEqual(id, 1)
        id = s.get_id_for_value("B", "B")
        self.assertEqual(id, 0)
        id = s.get_id_for_value("B", "B")
        self.assertEqual(id, 0)
        id = s.get_id_for_value("A", "A")
        self.assertEqual(id, 0)
        id = s.get_id_for_value("A", "B")
        self.assertEqual(id, 1)
        id = s.get_id_for_value("C", "A")
        self.assertEqual(id, 2)
        id = s.get_id_for_value("A", "A")
        self.assertEqual(id, 0)

        self.assertEqual(s.get_value_for_id(0, "A"), "A")
        self.assertEqual(s.get_value_for_id(1, "A"), "B")
        self.assertEqual(s.get_value_for_id(0, "B"), "B")
        self.assertEqual(s.get_value_for_id(2, "A"), "C")



    def test_get_data_frame(self):
        data = SchedulerData.create_from('../../../../input/performance_test.xlsx')
        s = SamplingDataHolder(data)
        s.get_data_frame()
        self.fail()


    def test_get_scheduler_data(self):
        data = SchedulerData.create_from('../../../../input/performance_test.xlsx')
        initial_df = data.dates.reset_index(drop=True)
        s = SamplingDataHolder(data)
        export_df = s.get_scheduler_data().dates.reset_index(drop=True)

        # Check if the two dataframes are identical
        self.assertTrue(initial_df.equals(export_df))


