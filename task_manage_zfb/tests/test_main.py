# -*- coding: utf-8 -*-
import unittest
import os

from task_manage_zfb.tests.helper_test import *

from task_manage_zfb.config import Config, MasterConfig, WorkerConfig, ConfigParserWithComments
from task_manage_zfb.errors import ConfigParserLackOfStartCommentError, ConfigParserBadCommentError, ConfigNotConfigFileError
from task_manage_zfb.main import _on_master, makeBucket

import task_manage_zfb.master_bucket as mb
import task_manage_zfb.worker_bucket as wb
      
class TestMain(unittest.TestCase):
    def setUp(self):
        self.my_master_config = MasterConfig(master_configfile_path)
        self.my_worker_config = WorkerConfig(worker_configfile_path)
        with open(normalfile_path, 'w') as normalfile:
            normalfile.write("test")
        with open(emptyfile_path, 'w') as emptyfile:
            emptyfile.write("")
            
    def test__on_master(self):
        self.assertTrue(_on_master(test_folder_path))
        self.my_master_config.write_configfile()
        self.assertTrue(_on_master(test_folder_path))
        self.my_worker_config.write_configfile()
        self.assertFalse(_on_master(test_folder_path))
                        
    def test_makeBucket_on_master(self):
        self.my_master_config.write_configfile()
        my_bucket = makeBucket('raz', test_folder_path)
        self.assertIsInstance(my_bucket, mb.TaskBucket)
        
    def test_makeBucket_on_worker(self):
        self.my_worker_config.write_configfile()
        my_bucket = makeBucket('raz', test_folder_path)
        self.assertIsInstance(my_bucket, wb.TaskBucket)
            
    def tearDown(self):
        clean_up()
        
if __name__ == '__main__':
    unittest.main()
    