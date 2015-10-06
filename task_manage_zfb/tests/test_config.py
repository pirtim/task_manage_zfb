import unittest
import sys
import os

from task_manage_zfb.config import Config, ConfigParserWithComments
from task_manage_zfb.errors import ConfigParserLackOfStartCommentError, ConfigParserBadCommentError

class TestConfigParserWithComments(unittest.TestCase):
    def setUp(self):
        self.config = ConfigParserWithComments()        
        self.config.add_section('Section')
        self.config.set('Section', 'key', 'value') 
        self.path = '.test_helper'
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
        self.config.add_start_comment('# moj komentarz\n# linia2')
        with open(self.path, 'wb') as configfile:
            self.config.write(configfile)   
        with open(self.path, 'rb') as configfile:
            file_content = configfile.readlines()
            self.assertEqual(file_content[0], '# moj komentarz\n')
            self.assertEqual(file_content[1], '# linia2\n')
            self.assertEqual(file_content[2], '[Section]\n') 
            
    def test_ConfigParser_add_start_comment_raises_error(self):
        self.assertRaises(ConfigParserBadCommentError, self.config.add_start_comment, 'comm')
        self.assertRaises(ConfigParserBadCommentError, self.config.add_start_comment, 'comm\ncomme2')
    
    def test_ConfigParser_start_get_start_comment(self):   
        self.config.add_start_comment('# moj komentarz\n# linia2')
        my_comment = self.config.get_start_comment()
        self.assertEqual(my_comment, '# moj komentarz\n# linia2')
        
    def test_ConfigParser_start_del_start_comment(self):   
        self.config.add_start_comment('# moj komentarz\n# linia2')
        self.config.del_start_comment()
        self.assertFalse(hasattr(self, '_start_comment_str'))
        
    def test_ConfigParser_start_del_start_comment_raises_error(self):
        self.assertRaises(ConfigParserLackOfStartCommentError, self.config.del_start_comment)
    
    def test_ConfigParser_start_get_start_comment_raises_error(self):
        self.assertRaises(ConfigParserLackOfStartCommentError, self.config.get_start_comment)
       
    def tearDown(self):
        os.remove(self.path)

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.my_config = Config()
        # self.my_config.make_file()
        pass
        
    def test_Config___init__(self):
        my_config2 = Config()
        self.assertIsInstance(my_config2, Config)
        
    def tearDown(self):
        # self.my_config.del_file()
        pass           
        
if __name__ == '__main__':
    unittest.main()
    