# -*- coding: utf-8 -*-
from __future__ import division

import os
import datetime
import uuid
import time
import logging
from collections import namedtuple

# Cyclic reference?
# http://eli.thegreenplace.net/2009/06/12/safely-using-destructors-in-python
# https://en.wikipedia.org/wiki/Dependency_injection
# Chyba usuniete.

from errors import TaskNotFoundError

class TaskResult(list):
    '''Container for results of one task.'''
    OneTaskRes = namedtuple('OneTaskRes', 'raw hex time')

    def __init__(self, task, task_start_time=None, *args):
        list.__init__(self, *args)
        if task_start_time == None:
            task_start_time = datetime.datetime.now()
        self.task = task
        self.task_start_time = task_start_time

    def add_task_result(self, result_raw, execution_datetime=None):
        '''Adds result of one execution of task.'''
        if execution_datetime == None:
            execution_datetime = datetime.datetime.now()
        self.append(self.OneTaskRes(result_raw, uuid.uuid1().hex, execution_datetime))

class TaskBucketResult(list):
    '''Container for results of tasks.'''
    TaskResDate = namedtuple('TaskResDate', 'task_rst time')

    def __init__(self, taskBucket, bucket_initialize_time=None, *args):
        list.__init__(self, *args)
        if bucket_initialize_time == None:
            bucket_initialize_time = datetime.datetime.now()
        self.taskBucket = taskBucket
        self.bucket_initialize_time = bucket_initialize_time

    def add_bucket_result(self, task_result, task_execution_datetime=None):
        '''Adds results of task to bucket of task results.'''
        if task_execution_datetime == None:
            task_execution_datetime = datetime.datetime.now()
        self.append(self.TaskResDate(task_result, task_execution_datetime))

class Task(object):
    '''Remembers function to execute, args and times of execution.'''
    def __init__(self, function, times_to_exec=1, *args, **kwargs):
        self.function = function
        self.exec_times = 0
        self.times_to_exec = times_to_exec
        self.args = args
        self.kwargs = kwargs

    def execute_task(self, ClsResult = TaskResult):
        '''Executes one task. It will connect via SSH to hosts.'''
        task_result = ClsResult(self)

        logging.info("Wykonuje funkcje " + self.function.__name__ + " (z argumentami" + str(self.args) + str(self.kwargs) + "):")

        for j in range(self.times_to_exec):

            logging.debug("po raz " + str(j))
            result_raw = self.function(*self.args, **self.kwargs)
            logging.info("z wynikiem: " + str(result_raw))

            task_result.add_task_result(result_raw)
        return task_result

    # do przeniesienia do mastera
    def _get_str_about(self):
        return self.function.__name__ + " - " + str(self.times_to_exec) + " - " + str(self.args) + " - " + str(self.kwargs)

class TaskBucket(object):
    '''Container for tasks to execute.'''
    def __init__(self, name):
        self.bucket = []
        self.name = name

    def execute(self, settings_file=None, output=os.path.abspath(__file__), ClsResult = TaskBucketResult):
        '''Executes bucket of tasks. Can take some time.'''
        logging.info('Wykonuje zadanie: ' + self.name + '.')

        bucket_result = ClsResult(self)
        for i in self.bucket:
            bucket_result.add_bucket_result(i.execute_task())
        return bucket_result

    def add_task(self, func, times_to_exec=1,  *args, **kwargs):
        '''Main way to add tasks to execute. This function desn't execute/calculate anything - lazy execution.'''
        self.bucket += [Task(func, times_to_exec, *args, **kwargs)]

    def get_task(self, task_id):
        '''Returns Task of task_id.'''
        if len(self.bucket) - 1 < task_id:
            raise TaskNotFoundError(task_id)
        else:
            return self.bucket[task_id]

    def del_task(self, task_id):
        '''Deletes Task of task_id.'''
        if len(self.bucket) - 1 < task_id:
            raise TaskNotFoundError(task_id)
        else:
            del self.bucket[task_id]

    # do przeniesienia do mastera
    def list_bucket(self):
        '''Lists bucket.'''
        return_str = '[ id - function name - times to execute - args - kwargs ]\n'

        for index, tsk in enumerate(self.bucket):
            return_str += "[ " + str(index) + " - " + tsk._get_str_about() + " ]\n"
        # [:-1] = without \n
        return return_str[:-1]
