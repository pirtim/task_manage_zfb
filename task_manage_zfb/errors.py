# -*- coding: utf-8 -*-
from __future__ import with_statement, division
import ConfigParser

class MyBaseError(BaseException):
    pass

class TaskNotFoundError(MyBaseError):
    '''Raise when a user references to non existing task.'''
    def __init__(self, task_id, message=None, *args):
        if message == None:
            self.message = "Task of id " + str(task_id) + " not found."
        else:
            self.message = message
        self.task_id = task_id
        super(TaskNotFoundError, self).__init__(self.message, *args)
        
class ConfigParserLackOfStartCommentError(ConfigParser.Error):
    def __init__(self, message=None, *args):
        if message == None:
            self.message = "Start comment was not declared."
        else:
            self.message = message
        super(ConfigParser.Error, self).__init__(self.message, *args)
    
class ConfigParserBadCommentError(ConfigParser.Error):
    def __init__(self, message=None, *args):
        if message == None:
            self.message = "First character in every line of comment isn't equal to # or ;."
        else:
            self.message = message
        super(ConfigParser.Error, self).__init__(self.message, *args)
        
class ConfigNotConfigFileError(MyBaseError):
    '''Raise when a user references to non existing task.'''
    def __init__(self, path, message=None, *args):
        if message == None:
            self.message = str(path) + " is not valid zfb_config file."
        else:
            self.message = message
        self.path = path
        super(MyBaseError, self).__init__(self.message, *args)