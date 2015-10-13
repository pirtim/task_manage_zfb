import unittest
import datetime
import uuid
import logging
from collections import namedtuple

from task_manage_zfb.master_bucket import MasterTaskBucket, MasterTask, MasterTaskBucketResult, MasterTaskResult
from task_manage_zfb.worker_bucket import TaskBucket, Task, TaskResult
from task_manage_zfb.errors import TaskNotFoundError

import helper_test as hp

def id_fun(x):
    return x

class TestMasterTaskBucketResult(unittest.TestCase):
    def setUp(self):
        self.my_bucket = MasterTaskBucket(name="test_name")
        self.my_bucket.add_task(hp.id_fun, 1, 1)
        self.my_bucket_result = self.my_bucket.execute()

    def test_MasterTaskBucketResult__get_tablestr_bucket_result(self):
        self.assertIsInstance(self.my_bucket_result._get_tablestr_bucket_result(), list)

    def test_MasterTaskBucketResult_get_table_bucket_result(self):
        self.assertIsInstance(self.my_bucket_result.get_table_bucket_result(), unicode)

class TestMasterTask(unittest.TestCase):
    def setUp(self):
        self.my_task = MasterTask(hp.id_fun, 2, 1)

    def test_MasterTask__get_str_about(self):
        my_str = self.my_task._get_str_about()
        self.assertEqual(my_str, 'id_fun - 2 - (1,) - {}')

    def test_MasterTask_execute_task(self):
        my_result = self.my_task.execute_task()
        self.assertIsInstance(my_result, MasterTaskResult)
        self.assertIsInstance(my_result[0].raw, int)
        self.assertIsInstance(my_result[0].hex, str)
        self.assertEqual(len(my_result[0].hex), len(uuid.uuid1().hex))
        self.assertIsInstance(my_result[0].time, datetime.date)
        self.assertEqual(self.my_task, my_result.task)
        self.assertEqual([i[0] for i in my_result], [1, 1])

class TestMasterTaskBucket(unittest.TestCase):
    def setUp(self):
        self.my_bucket = MasterTaskBucket(name="test_name")
        self.my_bucket.add_task(hp.id_fun, 1, 1)

    def test_MasterTaskBucket_execute_output_type(self):
        self.assertIsInstance(self.my_bucket.execute(), MasterTaskBucketResult)

    def test_MasterTaskBucket_list_bucket(self):
        my_str_list = self.my_bucket.list_bucket()
        assert_to = "[ id - function name - times to execute - args - kwargs ]\n[ 0 - id_fun - 1 - (1,) - {} ]"
        self.assertEqual(my_str_list, assert_to)


class TestMasterTaskBucket_Connection(unittest.TestCase):
    def setUp(self):
        self.my_bucket = MasterTaskBucket(name="test_name")
        self.my_bucket.add_task(hp.run_host_name)

    def test_MasterTaskBucket_execute_hostname(self):
        self.my_bucket_result = self.my_bucket.execute()
        my_one_result = self.my_bucket_result[0].task_rst[0].raw
        self.assertEqual(my_one_result, 'gene')

if __name__ == '__main__':
    unittest.main()
