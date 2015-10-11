# -*- coding: utf-8 -*-
#  https://docs.python.org/2/library/configparser.html
'''Contains custom ConfigParsers for worker and master environment.'''

from __future__ import division

import ConfigParser
import os
import sys
import logging

from errors import ConfigParserLackOfStartCommentError, ConfigParserBadCommentError, ConfigNotConfigFileError

class ConfigParserWithComments(ConfigParser.ConfigParser):
    '''ConfigParser with comment functionality.'''
    def set_start_comment(self, comment):
        r'''
        Sets start comment. Comment can be multiline.
        Raises TypeError if comment is not a string.
        Raises ConfigParserBadCommentError if every line of comment does not start with # or ;.
        
        Examples:
        >>> cpwc = ConfigParserWithComments()
        >>> cpwc.set_start_comment('# my_comment\n#second line')
        
        >>> cpwc.set_start_comment('# my_comment')
        >>> cpwc.get_start_comment()
        '# my_comment'
                
        >>> cpwc.set_start_comment('my_comment')
        Traceback (most recent call last):
            File "config.py", line 43, in set_start_comment
        ConfigParserBadCommentError: First character in every line of comment isn't equal to # or ;.
        
        >>> cpwc.set_start_comment(1)
        Traceback (most recent call last): 
            File "config.py", line 37, in set_start_comment           
        TypeError: Variable comment isn't string type.
        '''       
        if type(comment) != str:
            raise TypeError("Variable comment isn't string type.")
        
        splitted_comment = comment.splitlines()
        for line in splitted_comment:     
            #   line[0] != "#" and line[0] != ";":       
            if not (line.startswith("#") or line.startswith(";")):
                raise ConfigParserBadCommentError()
        self._start_comment_str = comment          
        
    def del_start_comment(self):
        '''
        Deletes earlier set start_comment.
        Raises ConfigParserLackOfStartCommentError if start_comment was not set.
        
        Examples:
        >>> cpwc = ConfigParserWithComments()
        >>> cpwc.set_start_comment('# my_comment')
        >>> cpwc.del_start_comment()
        
        >>> cpwc.del_start_comment()
        Traceback (most recent call last): 
            File "config.py", line 66, in del_start_comment
        ConfigParserLackOfStartCommentError: Start comment was not declared.
        '''
        
        if hasattr(self, '_start_comment_str'):
            del self._start_comment_str
        else:
            raise ConfigParserLackOfStartCommentError()
            
    def get_start_comment(self):
        '''
        Returns start comment as string.
         
        Examples:
        >>> cpwc = ConfigParserWithComments()
        >>> cpwc.set_start_comment('# my_comment')
        >>> cpwc.get_start_comment()
        '# my_comment'
        '''
        if hasattr(self, '_start_comment_str'):
            return self._start_comment_str
        else:
            raise ConfigParserLackOfStartCommentError()        
                
    def add_comment(self, section, comment):        
        '''
        Adds inline comment in section.
         
        Examples:
        >>> cpwc = ConfigParserWithComments()
        >>> cpwc.add_section('Section')
        >>> cpwc.add_comment('Section', 'my_comment')
        >>> cpwc.items('Section')
        [('# my_comment', None)]
        '''
        self.set(section, '# %s' % (comment,), None)
        
    def del_comment(self, section, comment):
        '''
        Deletes inline comment from section.
        Return True if comment existed, False otherwise.
         
        Examples:
        >>> cpwc = ConfigParserWithComments()
        >>> cpwc.add_section('Section')
        >>> cpwc.add_comment('Section', 'my_comment')
        >>> cpwc.del_comment('Section', 'my_comment')
        True
        
        >>> cpwc.del_comment('Section', 'my_comment')
        False
        
        >>> cpwc.del_comment('Section_other', 'my_comment')
        Traceback (most recent call last):
        NoSectionError: No section: 'Section_other'
        '''
        return self.remove_option(section, "# " + comment)
        
    def write(self, fp):
        '''Write an .ini-format representation of the configuration state.'''
        if hasattr(self, '_start_comment_str'):
            fp.write("%s\n" % self._start_comment_str)        
        if self._defaults:
            fp.write("[%s]\n" % ConfigParser.DEFAULTSECT)
            for (key, value) in self._defaults.items():
                self._write_item(fp, key, value)
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                self._write_item(fp, key, value)
            fp.write("\n")
            
    def _write_item(self, fp, key, value):
        if key.startswith('#') and value is None:
            fp.write("%s\n" % (key,))
        else:
            fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))

class Config(ConfigParserWithComments):
    '''Main config class. Parses zfb config files.'''
    
    # START not pythonic    
    internal_recognize_str = 'true'
    
    @staticmethod
    def _config_file_recognize_str_gen(internal_recognize_str):
        return '# -*- task_manage_zfb: {} -*-'.format(internal_recognize_str)
    
    _config_file_recognize_str = _config_file_recognize_str_gen.__func__(internal_recognize_str)    
    # END not pythonic
           
    def __init__(self, configfile_path, *args, **kwargs):
        self.configfile_path = configfile_path
        ConfigParserWithComments.__init__(self, *args, **kwargs)
    
    def write(self, fp):
        '''Write an .ini-format representation of the configuration state.'''      
        fp.write("%s\n" % self._config_file_recognize_str)
        ConfigParserWithComments.write(self, fp)
    
    @classmethod
    def is_config_file(cls, file_path, _config_file_recognize_str = _config_file_recognize_str):
        '''Returns True if file in file_path was written by Config.write_configfile.'''        
        if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
            return False   
        with open(file_path, 'rb') as configfile:
            return configfile.readline().strip() == _config_file_recognize_str

    def write_configfile(self, file_path=None):
        '''Write an .ini-format representation of the configuration state to file under file_path.'''
        if file_path == None:
            file_path = self.configfile_path
        with open(file_path, 'wb') as configfile:
            self.write(configfile)
        
        # DEBUG CODE: 
        # with open(file_path, 'rb') as configfile:
        #     print 'configfile.read():'
        #     print configfile.read()    
        #     print '=========='        
            
    def del_configfile(self, file_path=None):
        '''Deletes file in file_path if file was written by Config.write_configfile.''' 
        if file_path == None:
            file_path = self.configfile_path
        if Config.is_config_file(file_path):
            os.remove(file_path)
        else:
            raise ConfigNotConfigFileError(file_path)                
    
class MasterConfig(Config):
    '''
    Parses master config files.
    Looks for config file in main master directory or in dirictory specified by user.
    '''
    internal_recognize_str = 'master'
    _config_file_recognize_str = Config._config_file_recognize_str_gen(internal_recognize_str)
    
    @classmethod
    def is_config_file(cls, file_path, _config_file_recognize_str = _config_file_recognize_str):
        '''Returns True if file in file_path was written by MasterConfig.write_configfile.'''
        return Config.is_config_file(file_path, _config_file_recognize_str)
        
    def __init__(self, configfile_path, *args, **kwargs):
        Config.__init__(self, configfile_path, *args, **kwargs)
        self.ssh_comment = 'txt'
        
        # a moze po prostu fabricrc zmodyfikowany z wyraznym zaznaczeniem co mozna a czego nie mozna?
        self.add_section('SSH')
        self.add_comment('SSH', 'ssh config')
        self.set('SSH', 'user', '<TO DEFINE> # not required')
        self.set('SSH', 'password', '<TO DEFINE> # not required')
        self.set('SSH', 'gateway', '<TO DEFINE> # not required, example: host.com or user@host.com')
        self.set('SSH', 'hosts_list', '<TO DEFINE> # required, example: [host1.com, user@host2.com]')
        
    def is_masterconfig_ready(self, configfile_path=None):
        if configfile_path == None:
            configfile_path = self.configfile_path
        return True
    
class WorkerConfig(Config):
    '''
    Creates and parses worker config files.    
    Looks for config file in worker main directory or in directory specified by user.
    '''
    internal_recognize_str = 'worker'
    _config_file_recognize_str = Config._config_file_recognize_str_gen(internal_recognize_str)
    
    @classmethod
    def is_config_file(cls, file_path, _config_file_recognize_str = _config_file_recognize_str):
        '''Returns True if file in file_path was written by WorkerConfig.write_configfile.'''
        return Config.is_config_file(file_path, _config_file_recognize_str)
        
if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={})
    