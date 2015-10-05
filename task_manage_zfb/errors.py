# -*- coding: utf-8 -*-
from __future__ import with_statement, division

class TaskNotFoundError(IndexError):
    '''Raise when a user references to non existing task.'''
    def __init__(self, task_id, message=None, *args):
        if message == None:
            self.message = "Task of id " + str(task_id) + " not found."
        else:
            self.message = message
        self.task_id = task_id
        super(TaskNotFoundError, self).__init__(self.message, *args)
        