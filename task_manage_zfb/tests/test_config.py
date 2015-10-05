import unittest
import datetime
import uuid
from task_manage_zfb.bucket import TaskBucket

class TestConfig(unittest.TestCase):
    def setUp(self):
        pass        
        
    def test_Task__get_str_about(self):        
        self.assertIsInstance(1, int)
        self.assertEqual(1, 1)
        
    def TearDown(self):
        pass           
        
if __name__ == '__main__':
    unittest.main()
    