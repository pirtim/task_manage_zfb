import unittest
import datetime
import uuid

from task_manage_zfb.master_bucket import MasterTaskBucket, MasterTask, MasterTaskBucketResult, MasterTaskResult
from task_manage_zfb.worker_bucket import TaskBucket, Task, TaskResult
from task_manage_zfb.errors import TaskNotFoundError

def id_fun(x):
    return x
 
class TestMasterTask(unittest.TestCase):
    def setUp(self):
        self.my_task = MasterTask(id_fun, 2, 1)
        
    def test_MasterTask__get_str_about(self):
        my_str = self.my_task._get_str_about()
        self.assertEqual(my_str, 'id_fun - 2 - (1,) - {}')
        
    def test_MasterTask_execute_task(self):
        my_result = self.my_task.execute_task()
        self.assertIsInstance(my_result, MasterTaskResult)
        self.assertIsInstance(my_result.task_result[0][0], int)
        self.assertIsInstance(my_result.task_result[0][1], str)
        self.assertEqual(len(my_result.task_result[0][1]), len(uuid.uuid1().hex))
        self.assertIsInstance(my_result.task_result[0][2], datetime.date)
        self.assertEqual(self.my_task, my_result.task)
        self.assertEqual([i[0] for i in my_result.task_result], [1, 1])
 
class TestMasterTaskBucket(unittest.TestCase):
    def setUp(self):
        self.my_bucket = MasterTaskBucket(name="test_name")
        self.my_bucket.add_task(id_fun, 1, 1)
 
    def test_MasterTaskBucket_execute(self):
        self.assertIsInstance(self.my_bucket.execute(), MasterTaskBucketResult)
               
    def test_MasterTaskBucket_list_bucket(self):
        my_str_list = self.my_bucket.list_bucket()
        assert_to = "[ id - function name - times to execute - args - kwargs ]\n[ 0 - id_fun - 1 - (1,) - {} ]"
        self.assertEqual(my_str_list, assert_to)
        
class TestMasterTaskBucketResult(unittest.TestCase):
    def setUp(self):
        self.my_bucket = MasterTaskBucket(name="test_name")
        self.my_bucket.add_task(id_fun, 1, 1)
        self.my_bucket_result = self.my_bucket.execute()
                
    def test_MasterTaskBucketResult__get_str_bucket_result(self):
        self.assertIsInstance(self.my_bucket_result._get_str_bucket_result, str)
        
    def test_MasterTaskBucketResult_get_table_bucket_result(self):
        self.assertIsInstance(self.my_bucket_result.get_table_bucket_result(), str)
        
if __name__ == '__main__':
    unittest.main()
    