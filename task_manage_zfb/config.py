# -*- coding: utf-8 -*-
#  https://docs.python.org/2/library/configparser.html
from __future__ import with_statement, division

from errors import ConfigParserLackOfStartCommentError, ConfigParserBadCommentError
import ConfigParser
import os
import sys

class ConfigParserWithComments(ConfigParser.ConfigParser):  
    def add_start_comment(self, comment):
        splitted_comment = comment.splitlines()
        for line in splitted_comment:            
            if not (line.startswith("#") or line.startswith(";")):#   line[0] != "#" and line[0] != ";":
                raise ConfigParserBadCommentError()
        self._start_comment_str = comment      
        
    def del_start_comment(self):
        if hasattr(self, '_start_comment_str'):
            del self._start_comment_str
        else:
            raise ConfigParserLackOfStartCommentError()
            
    def get_start_comment(self):
        if hasattr(self, '_start_comment_str'):
            return self._start_comment_str
        else:
            raise ConfigParserLackOfStartCommentError()            
                
    def add_comment(self, section, comment):
        self.set(section, '# %s' % (comment,), None)  
        
    def write(self, fp):
        """Write an .ini-format representation of the configuration state.""" 
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

class Config():
    '''Main config class. Parses config files.'''
    def __init__(self, config_file_path=None):
        self.config_file_path = config_file_path
    
class MasterConfig(Config):
    '''
    Parses master config files.
    Looks for config file in main master directory or in dirictory specified by user.
    '''
    
class WorkerConfig(Config):
    '''
    Creates and parses worker config files.    
    Looks for config file in worker main directory or in directory specified by user.
    '''
    
class ConnectionConfig(Config):
    '''
    Creates and parse connection config files.    
    Looks for config file in main master, worker directory or in directory specified by user.
    '''