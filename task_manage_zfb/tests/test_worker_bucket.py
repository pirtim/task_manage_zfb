import unittest
import datetime
import uuid
import logging

from task_manage_zfb.worker_bucket import TaskBucket, Task, TaskResult, TaskBucketResult
from task_manage_zfb.errors import TaskNotFoundError

def id_fun(x):
    return x
 
class TestTask(unittest.TestCase):
    def setUp(self):
        self.my_task = Task(id_fun, 2, 1)
        
    def test_Task__get_str_about(self):
        my_str = self.my_task._get_str_about()
        self.assertEqual(my_str, 'id_fun - 2 - (1,) - {}')
        
    def test_Task_execute_task(self):
        my_result = self.my_task.execute_task()
        self.assertIsInstance(my_result, TaskResult)              
        self.assertIsInstance(my_result.task_result[0][0], int)    
        self.assertIsInstance(my_result.task_result[0][1], str)        
        self.assertEqual(len(my_result.task_result[0][1]), len(uuid.uuid1().hex))
        self.assertIsInstance(my_result.task_result[0][2], datetime.date)
        self.assertEqual(self.my_task, my_result.task)
        self.assertEqual([i[0] for i in my_result.task_result], [1, 1])
 
class TestTaskBucket(unittest.TestCase):        
    def setUp(self):
        self.my_bucket = TaskBucket(name="test_name")        
        self.my_bucket.add_task(id_fun, 1, 1)
 
    def test_TaskBucket_add_task(self):
        self.my_bucket.add_task(id_fun, 1)
            
        self.assertEqual(2, len(self.my_bucket.bucket))
        self.assertIn(id_fun, [tsk.function for tsk in self.my_bucket.bucket])
        
    def test_TaskBucket_add_task_correct_Type(self):
        for i in self.my_bucket.bucket:
            self.assertIsInstance(i, Task)           
     
    def test_TaskBucket_get_task_raise_error(self):
        self.assertRaises(TaskNotFoundError, self.my_bucket.get_task, 1)  
            
    def test_TaskBucket_get_task(self):
        self.my_task = self.my_bucket.get_task(0)
        self.assertEqual(self.my_task.function, id_fun)
        self.assertEqual(self.my_task.times_to_exec, 1)  
               
    def test_TaskBucket_list_bucket(self):
        my_str_list = self.my_bucket.list_bucket()
        assert_to = "[ id - function name - times to execute - args - kwargs ]\n[ 0 - id_fun - 1 - (1,) - {} ]"
        self.assertEqual(my_str_list, assert_to)
    
    def test_TaskBucket_del_task(self):        
        self.my_task = self.my_bucket.get_task(0)      
        self.my_bucket.del_task(0)
        self.assertNotIn(self.my_task, self.my_bucket.bucket)
        
    def test_TaskBucket_execute(self):
        self.assertIsInstance(self.my_bucket.execute(), TaskBucketResult)
        
class TestTaskBucketResult(unittest.TestCase):
    def setUp(self):
        self.my_bucket = TaskBucket(name="test_name")
        self.my_bucket.add_task(id_fun, 1, 1)
        self.my_bucket_result = self.my_bucket.execute()
        
if __name__ == '__main__':
    unittest.main()
    