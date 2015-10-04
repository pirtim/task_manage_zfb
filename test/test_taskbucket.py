import unittest
from task_manage_zfb import TaskBucket, Task, TaskNotFoundError
 
class TestTaskBucket(unittest.TestCase):
    
    @staticmethod
    def id_fun(x):
        return x
        
    def setUp(self):
        self.my_bucket = TaskBucket(name="test_name")        
        self.my_bucket.add_task(self.id_fun, 1)
 
    def test_TaskBucket_add_task(self):
        self.my_bucket.add_task(self.id_fun, 1)
            
        self.assertEqual(2, len(self.my_bucket.bucket))
        self.assertIn(self.id_fun, [tsk.function for tsk in self.my_bucket.bucket])
        
    def test_TaskBucket_add_task_correct_Type(self):
        for i in self.my_bucket.bucket:
            self.assertIsInstance(i, Task)           
     
    def test_TaskBucket_get_task_raise_error(self):
        self.assertRaises(TaskNotFoundError, self.my_bucket.get_task, 1)  
            
    def test_TaskBucket_get_task(self):
        self.my_task = self.my_bucket.get_task(0)
        self.assertEqual(self.my_task.function, self.id_fun)
        self.assertEqual(self.my_task.times_to_exec, 1)  
               
    def test_TaskBucket_list_bucket(self):
        my_str_list = self.my_bucket.list_bucket()
        assert_to = "[ id - function name - times to execute - args - kwargs ]\n[ 0 - id_fun - 1 - () - {} ]"
        self.assertEqual(my_str_list, assert_to)
    
    def test_TaskBucket_del_task(self):        
        self.my_task = self.my_bucket.get_task(0)      
        self.my_bucket.del_task(0)
        self.assertNotIn(self.my_task, self.my_bucket.bucket)
        
if __name__ == '__main__':
    unittest.main()