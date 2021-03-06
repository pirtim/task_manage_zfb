import unittest
import datetime
import uuid
import logging

from task_manage_zfb.worker_bucket import Bucket, Task, TaskResult, BucketResult
from task_manage_zfb.errors import TaskNotFoundError

import helper_test as hp

class TestTask(unittest.TestCase):
    def setUp(self):
        self.my_task = Task(hp.id_fun, 2, 1)

    def test_Task__get_str_about(self):
        my_str = self.my_task._get_str_about()
        self.assertEqual(my_str, 'id_fun - 2 - (1,) - {}')

    def test_Task_execute_task(self):
        my_result = self.my_task.execute_task()
        self.assertIsInstance(my_result, TaskResult)
        self.assertIsInstance(my_result[0].raw, int)
        self.assertIsInstance(my_result[0].hex, str)
        self.assertEqual(len(my_result[0].hex), len(uuid.uuid1().hex))
        self.assertIsInstance(my_result[0].time, datetime.date)
        self.assertEqual(self.my_task, my_result.task)
        self.assertEqual([i[0] for i in my_result], [1, 1])

class TestBucket(unittest.TestCase):
    def setUp(self):
        self.my_bucket = Bucket(name="test_name")
        self.my_bucket.add_task(hp.id_fun, 1, 1)

    def test_Bucket_add_task(self):
        self.my_bucket.add_task(hp.id_fun, 1)

        self.assertEqual(2, len(self.my_bucket.bucket))
        self.assertIn(hp.id_fun, [tsk.function for tsk in self.my_bucket.bucket])

    def test_Bucket_add_task_correct_Type(self):
        for i in self.my_bucket.bucket:
            self.assertIsInstance(i, Task)

    def test_Bucket_get_task_raise_error(self):
        self.assertRaises(TaskNotFoundError, self.my_bucket.get_task, 1)

    def test_Bucket_get_task(self):
        self.my_task = self.my_bucket.get_task(0)
        self.assertEqual(self.my_task.function, hp.id_fun)
        self.assertEqual(self.my_task.times_to_exec, 1)

    def test_Bucket_list_bucket(self):
        my_str_list = self.my_bucket.list_bucket()
        assert_to = "[ id - function name - times to execute - args - kwargs ]\n[ 0 - id_fun - 1 - (1,) - {} ]"
        self.assertEqual(my_str_list, assert_to)

    def test_Bucket_del_task(self):
        self.my_task = self.my_bucket.get_task(0)
        self.my_bucket.del_task(0)
        self.assertNotIn(self.my_task, self.my_bucket.bucket)

    def test_Bucket_execute(self):
        self.assertIsInstance(self.my_bucket.execute(), BucketResult)

class TestBucket_Connection(unittest.TestCase):
    def setUp(self):
        self.my_bucket = Bucket(name="test_name")
        self.my_bucket.add_task(hp.run_host_name)

    def test_Bucket_execute_hostname(self):
        self.my_bucket_result = self.my_bucket.execute()
        my_one_result = self.my_bucket_result[0].task_rst[0].raw
        self.assertEqual(my_one_result, hp.local_hostname)

if __name__ == '__main__':
    unittest.main()
