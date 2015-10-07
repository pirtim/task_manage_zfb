# -*- coding: utf-8 -*-
import unittest
import os

from task_manage_zfb.config import Config, MasterConfig, WorkerConfig, ConfigParserWithComments
from task_manage_zfb.errors import ConfigParserLackOfStartCommentError, ConfigParserBadCommentError, ConfigNotConfigFileError


_test_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files_gitignore')

def delete_if_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)

class TestConfigParserWithComments(unittest.TestCase):
    def setUp(self):
        self.config = ConfigParserWithComments()        
        self.config.add_section('Section')
        self.config.set('Section', 'key', 'value')
        self.path = os.path.join(_test_folder_path, '.test_helper')
        with open(self.path, 'wb') as configfile:
            configfile.write('')
      
    def test_ConfigParser_add_comment(self):
        self.config.add_comment('Section', 'this is the comment')   
        self.config.set('Section', 'key', 'value')     
        with open(self.path, 'wb') as configfile:
            self.config.write(configfile)
        with open(self.path, 'rb') as configfile:
            file_content = configfile.readlines()
            self.assertEqual(file_content[0], '[Section]\n')
            self.assertEqual(file_content[1], 'key = value\n')
            self.assertEqual(file_content[2], '# this is the comment\n')
         
    def test_ConfigParser_add_start_comment(self):   
        self.config.set_start_comment('# moj komentarz\n# linia2')
        with open(self.path, 'wb') as configfile:
            self.config.write(configfile)   
        with open(self.path, 'rb') as configfile:
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
        delete_if_file(self.path)

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test_configfile_path = os.path.join(_test_folder_path, '.conf_file')
        self.normalfile_path = os.path.join(_test_folder_path, '.normal_file')
        self.emptyfile_path = os.path.join(_test_folder_path, '.empty_file')
        self.my_config = Config(self.test_configfile_path)
        with open(self.normalfile_path, 'w') as normalfile:
            normalfile.write("test")
        with open(self.emptyfile_path, 'w') as emptyfile:
            emptyfile.write("")
        
    def test_Config___init__(self):
        my_config2 = Config(self.test_configfile_path)
        self.assertIsInstance(my_config2, Config)
        self.assertIsInstance(my_config2.confpars_inst, ConfigParserWithComments)
        self.assertEqual(my_config2.configfile_path, self.test_configfile_path)
        
    def test_Config_write_configfile(self):
        # order matters
        self.assertFalse(os.path.isfile(self.test_configfile_path))
        self.my_config.write_configfile()
        self.assertTrue(os.path.isfile(self.test_configfile_path))
        with open(self.test_configfile_path, 'rb') as configfile: 
            self.assertEqual(configfile.read(), '# -*- task_manage_zfb: true -*-\n')
        self.assertEqual(os.path.getsize(self.test_configfile_path), 32L)    
        
    def test_Config_write_configfile2(self):
        # order matters
        self.assertFalse(os.path.isfile(self.test_configfile_path))
        self.my_config.confpars_inst.set_start_comment('# sth to comment')
        self.my_config.write_configfile()
        self.assertTrue(os.path.isfile(self.test_configfile_path))
        with open(self.test_configfile_path, 'rb') as configfile: 
            self.assertEqual(configfile.read(), '# -*- task_manage_zfb: true -*-\n# sth to comment\n')
        self.assertEqual(os.path.getsize(self.test_configfile_path), 49L)      
    
    def test_Config_is_Config_File(self):
        self.my_config.write_configfile()
        self.assertFalse(Config.is_Config_File(self.normalfile_path))
        self.assertTrue(Config.is_Config_File(self.test_configfile_path))
        
    def test_Config_del_configfile(self):
        self.my_config.write_configfile()
        self.assertTrue(os.path.isfile(self.test_configfile_path))
        self.my_config.del_configfile()
        self.assertFalse(os.path.isfile(self.test_configfile_path))

    def test_Config_del_configfile_raises_error(self):
        self.assertTrue(os.path.isfile(self.normalfile_path))
        self.assertRaises(ConfigNotConfigFileError, self.my_config.del_configfile, self.normalfile_path)
        self.assertTrue(os.path.isfile(self.normalfile_path))
                
    def tearDown(self):
        delete_if_file(self.test_configfile_path)
        delete_if_file(self.normalfile_path)
        delete_if_file(self.emptyfile_path)
        
class TestMasterConfig(unittest.TestCase):
    def setUp(self):
        self.test_configfile_path = os.path.join(_test_folder_path, '.conf_file')
        self.normalfile_path = os.path.join(_test_folder_path, '.normal_file')
        self.emptyfile_path = os.path.join(_test_folder_path, '.empty_file')
        self.my_config = MasterConfig(self.test_configfile_path)
        with open(self.normalfile_path, 'w') as normalfile:
            normalfile.write("test")
        with open(self.emptyfile_path, 'w') as emptyfile:
            emptyfile.write("")
            
    def test_Config_write_configfile(self):
        self.assertFalse(os.path.isfile(self.test_configfile_path))
        self.my_config.write_configfile()
        self.assertTrue(os.path.isfile(self.test_configfile_path))
        with open(self.test_configfile_path, 'rb') as configfile: 
            self.assertEqual(configfile.read(), '# -*- task_manage_zfb: master -*-\n')
        self.assertEqual(os.path.getsize(self.test_configfile_path), 34L)    
            
    def tearDown(self):
        delete_if_file(self.test_configfile_path)
        delete_if_file(self.normalfile_path)
        delete_if_file(self.emptyfile_path)
        
class TestMasterConfig(unittest.TestCase):
    def setUp(self):
        self.test_configfile_path = os.path.join(_test_folder_path, '.conf_file')
        self.normalfile_path = os.path.join(_test_folder_path, '.normal_file')
        self.emptyfile_path = os.path.join(_test_folder_path, '.empty_file')
        self.my_config = WorkerConfig(self.test_configfile_path)
        with open(self.normalfile_path, 'w') as normalfile:
            normalfile.write("test")
        with open(self.emptyfile_path, 'w') as emptyfile:
            emptyfile.write("")
            
    def test_Config_write_configfile(self):
        self.assertFalse(os.path.isfile(self.test_configfile_path))
        self.my_config.write_configfile()
        self.assertTrue(os.path.isfile(self.test_configfile_path))
        with open(self.test_configfile_path, 'rb') as configfile: 
            self.assertEqual(configfile.read(), '# -*- task_manage_zfb: worker -*-\n')
        self.assertEqual(os.path.getsize(self.test_configfile_path), 34L)    
            
    def tearDown(self):
        delete_if_file(self.test_configfile_path)
        delete_if_file(self.normalfile_path)
        delete_if_file(self.emptyfile_path)                
        
if __name__ == '__main__':
    unittest.main()
    