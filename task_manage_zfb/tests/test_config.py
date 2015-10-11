# -*- coding: utf-8 -*-
import unittest
import os

from task_manage_zfb.tests.helper_test import *

from task_manage_zfb.config import Config, MasterConfig, WorkerConfig, ConfigParserWithComments
from task_manage_zfb.errors import ConfigParserLackOfStartCommentError, ConfigParserBadCommentError, ConfigNotConfigFileError

class TestConfigParserWithComments(unittest.TestCase):
    def setUp(self):        
        help_set_up()
        self.config = ConfigParserWithComments()        
        self.config.add_section('Section')
        self.config.set('Section', 'key', 'value')
        with open(test_configfile_path, 'wb') as configfile:
            configfile.write('')
      
    def test_ConfigParser_add_comment(self):
        self.config.add_comment('Section', 'this is the comment')   
        self.config.set('Section', 'key', 'value')     
        with open(test_configfile_path, 'wb') as configfile:
            self.config.write(configfile)
        with open(test_configfile_path, 'rb') as configfile:
            file_content = configfile.readlines()
            self.assertEqual(file_content[0], '[Section]\n')
            self.assertEqual(file_content[1], 'key = value\n')
            self.assertEqual(file_content[2], '# this is the comment\n')
         
    def test_ConfigParser_add_start_comment(self):   
        self.config.set_start_comment('# moj komentarz\n# linia2')
        with open(test_configfile_path, 'wb') as configfile:
            self.config.write(configfile)   
        with open(test_configfile_path, 'rb') as configfile:
            file_content = configfile.readlines()
            self.assertEqual(file_content[0], '# moj komentarz\n')
            self.assertEqual(file_content[1], '# linia2\n')
            self.assertEqual(file_content[2], '[Section]\n') 
            
    def test_ConfigParser_add_start_comment_raises_error(self):
        self.assertRaises(TypeError, self.config.set_start_comment, 1)
        self.assertRaises(ConfigParserBadCommentError, self.config.set_start_comment, 'comm')
        self.assertRaises(ConfigParserBadCommentError, self.config.set_start_comment, 'comm\ncomme2')
    
    def test_ConfigParser_start_get_start_comment(self):   
        self.config.set_start_comment('# moj komentarz\n# linia2')
        my_comment = self.config.get_start_comment()
        self.assertEqual(my_comment, '# moj komentarz\n# linia2')
        
    def test_ConfigParser_start_del_start_comment(self):   
        self.config.set_start_comment('# moj komentarz\n# linia2')
        self.config.del_start_comment()
        self.assertFalse(hasattr(self, '_start_comment_str'))
        
    def test_ConfigParser_start_del_start_comment_raises_error(self):
        self.assertRaises(ConfigParserLackOfStartCommentError, self.config.del_start_comment)
    
    def test_ConfigParser_start_get_start_comment_raises_error(self):
        self.assertRaises(ConfigParserLackOfStartCommentError, self.config.get_start_comment)
       
    def tearDown(self):
        help_tear_down()

class TestConfig(unittest.TestCase):
    def setUp(self):
        help_set_up()
        self.my_config = Config(test_configfile_path)
        
    def test_Config___init__(self):
        my_config2 = Config(test_configfile_path)
        self.assertIsInstance(my_config2, Config)
        self.assertIsInstance(my_config2, ConfigParserWithComments)
        self.assertEqual(my_config2.configfile_path, test_configfile_path)
        
    def test_Config_write_configfile(self):
        # order matters
        self.assertFalse(os.path.isfile(test_configfile_path))
        self.my_config.write_configfile()
        self.assertTrue(os.path.isfile(test_configfile_path))
        with open(test_configfile_path, 'rb') as configfile: 
            self.assertEqual(configfile.read(), '# -*- task_manage_zfb: true -*-\n')
        self.assertEqual(os.path.getsize(test_configfile_path), 32L)    
        
    def test_Config_write_configfile2(self):
        # order matters
        self.assertFalse(os.path.isfile(test_configfile_path))
        self.my_config.set_start_comment('# sth to comment')
        self.my_config.write_configfile()
        self.assertTrue(os.path.isfile(test_configfile_path))
        with open(test_configfile_path, 'rb') as configfile: 
            self.assertEqual(configfile.read(), '# -*- task_manage_zfb: true -*-\n# sth to comment\n')
        self.assertEqual(os.path.getsize(test_configfile_path), 49L)      
    
    def test_Config_is_config_file(self):
        self.my_config.write_configfile()
        self.assertFalse(Config.is_config_file(normalfile_path))
        self.assertTrue(Config.is_config_file(test_configfile_path))
        
    def test_Config_del_configfile(self):
        self.my_config.write_configfile()
        self.assertTrue(os.path.isfile(test_configfile_path))
        self.my_config.del_configfile()
        self.assertFalse(os.path.isfile(test_configfile_path))

    def test_Config_del_configfile_raises_error(self):
        self.assertTrue(os.path.isfile(normalfile_path))
        self.assertRaises(ConfigNotConfigFileError, self.my_config.del_configfile, normalfile_path)
        self.assertTrue(os.path.isfile(normalfile_path))
                
    def tearDown(self):
        help_tear_down()
        
class TestMasterConfig(unittest.TestCase):
    def setUp(self):
        help_set_up()
        self.my_config = MasterConfig(test_configfile_path)
            
    def test_MasterConfig_write_configfile(self):
        self.assertFalse(os.path.isfile(test_configfile_path))
        self.my_config.write_configfile()
        self.assertTrue(os.path.isfile(test_configfile_path))
        with open(test_configfile_path, 'rb') as configfile: 
            self.assertEqual(configfile.readline(), '# -*- task_manage_zfb: master -*-\n')
            self.assertEqual(configfile.readline(), '[SSH]\n')
        self.assertEqual(os.path.getsize(test_configfile_path), 273L)
        
    def test_MasterConfig_ready(self):
        pass
        
    def test_MasterConfig_is_config_file(self):
        self.my_config.write_configfile()
        self.assertFalse(MasterConfig.is_config_file(normalfile_path))
        self.assertTrue(MasterConfig.is_config_file(test_configfile_path))              
            
    def tearDown(self):
        help_tear_down()
        
class TestWorkerConfig(unittest.TestCase):
    def setUp(self):
        help_set_up()
        self.my_config = WorkerConfig(test_configfile_path)
            
    def test_WorkerConfig_write_configfile(self):
        self.assertFalse(os.path.isfile(test_configfile_path))
        self.my_config.write_configfile()
        self.assertTrue(os.path.isfile(test_configfile_path))
        with open(test_configfile_path, 'rb') as configfile: 
            self.assertEqual(configfile.read(), '# -*- task_manage_zfb: worker -*-\n')
        self.assertEqual(os.path.getsize(test_configfile_path), 34L)
        
    def test_WorkerConfig_is_config_file(self):
        self.my_config.write_configfile()
        self.assertFalse(WorkerConfig.is_config_file(normalfile_path))
        self.assertTrue(WorkerConfig.is_config_file(test_configfile_path))
            
    def tearDown(self):
        help_tear_down()       
        
if __name__ == '__main__':
    unittest.main()
    