# -*- coding: utf-8 -*-
#  https://docs.python.org/2/library/configparser.html
from __future__ import with_statement, division

from errors import ConfigParserLackOfStartCommentError, ConfigParserBadCommentError, ConfigNotConfigFileError
import ConfigParser
import os
import sys

class ConfigParserWithComments(ConfigParser.ConfigParser):  
    def add_start_comment(self, comment):
        if type(comment) != str:
            raise TypeError("Variable comment isn't string type.")
        
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

class Config:
    '''Main config class. Parses config files.'''    
    @staticmethod
    def _config_file_recognize_str_gen(internal_recognize_str): 
        return '# -*- task_manage_zfb: {} -*-\n'.format(internal_recognize_str)
    
    internal_recognize_str = 'true'
    # not pythonic
    _config_file_recognize_str = _config_file_recognize_str_gen.__func__(internal_recognize_str)
    
    @classmethod
    def _is_Config_File(cls, file_path):
        if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
            return False    
        with open(file_path, 'rb') as configfile:
            return configfile.readline() == cls._config_file_recognize_str
    
    def __init__(self, configfile_path):
        self.configfile_path = configfile_path
        self.confpars_inst = ConfigParserWithComments()   
        
    def write_configfile(self, file_path=None):
        if file_path == None:
            file_path = self.configfile_path
        with open(file_path, 'wb') as configfile:
            # broken add_start_comment here
            # -1 bo \n\n na koncu - przemyslec
            self.confpars_inst.add_start_comment(self._config_file_recognize_str[:-1])
            self.confpars_inst.write(configfile)
            
        # with open(file_path, 'rb') as configfile:
        #     print 'configfile.read():'
        #     print configfile.read()
            
            
    def del_configfile(self, file_path=None):
        if file_path == None:
            file_path = self.configfile_path
        if os.path.isfile(file_path):
            if Config._is_Config_File(file_path):
                os.remove(file_path)
            else:
                raise ConfigNotConfigFileError(file_path)
                
    
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
    
# chyba nie potrzebne, bedzie w masterze w sekcji ssh
class ConnectionConfig(Config):
    '''
    Creates and parse connection config files.    
    Looks for config file in main master, worker directory or in directory specified by user.
    '''
    