# -*- coding: utf-8 -*-
import unittest
import os
import logging

from task_manage_zfb.tests.helper_test import *

from task_manage_zfb.config import Config, MasterConfig, WorkerConfig, ConfigParserWithComments
from task_manage_zfb.errors import ConfigParserLackOfStartCommentError, ConfigParserBadCommentError, ConfigNotConfigFileError
from task_manage_zfb.main import _on_worker, Bucket

import task_manage_zfb.master_bucket as mb
import task_manage_zfb.worker_bucket as wb

class TestMain(unittest.TestCase):
    def setUp(self):
        self.my_master_config = MasterConfig(master_configfile_path)
        self.my_worker_config = WorkerConfig(worker_configfile_path)
        help_set_up()

    def test__on_worker(self):
        self.assertFalse(_on_worker(test_folder_path))
        self.my_master_config.write_configfile()
        self.assertFalse(_on_worker(test_folder_path))
        self.my_worker_config.write_configfile()
        self.assertTrue(_on_worker(test_folder_path))

    def test_makeBucket_on_master(self):
        self.my_master_config.write_configfile()
        my_bucket = Bucket('raz', test_folder_path)
        self.assertIsInstance(my_bucket, mb.MasterBucket)

    def test_makeBucket_on_master_local_test(self):
        self.my_master_config.write_configfile()
        my_bucket = Bucket('raz', test_folder_path, True)
        self.assertIsInstance(my_bucket, wb.Bucket)

    def test_makeBucket_on_worker(self):
        self.my_worker_config.write_configfile()
        my_bucket = Bucket('raz', test_folder_path)
        self.assertIsInstance(my_bucket, wb.Bucket)

    def tearDown(self):
        help_tear_down()

if __name__ == '__main__':
    unittest.main()
