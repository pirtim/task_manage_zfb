# -*- coding: utf-8 -*-
from __future__ import division
# from fabric.api import run, env, local, settings, abort, execute
# from fabric.contrib.console import confirm
# from fabric.contrib.project import rsync_project
# from fabric.decorators import runs_once
# from fabric.context_managers import hide
# Cyclic reference? 
# http://eli.thegreenplace.net/2009/06/12/safely-using-destructors-in-python
# https://en.wikipedia.org/wiki/Dependency_injection

from errors import TaskNotFoundError

import terminaltables
import os
import datetime
import uuid
import random
import time

class TaskResult(object):
    '''Container for results of one task.'''
    def __init__(self, task, task_start_time=None):
        if task_start_time == None:
            task_start_time = datetime.datetime.now()        
        self.task = task
        self.task_start_time = task_start_time
        self.task_result = []
        
    def add_task_result(self, result_raw, execution_datetime=None):
        '''Adds result of one execution of task.'''
        if execution_datetime == None:
            execution_datetime = datetime.datetime.now()
        self.task_result += [(result_raw, uuid.uuid1().hex, execution_datetime)]

class Task(object):
    '''Remembers function to execute, args and times of execution.'''
    def __init__(self, function, times_to_exec=1, *args, **kwargs):
        self.function = function
        self.exec_times = 0        
        self.times_to_exec = times_to_exec
        self.args = args
        self.kwargs = kwargs
    
    def execute_task(self, verbose = False):
        '''Executes one task. It will connect via SSH to hosts.'''  
        self.task_result = TaskResult(self)
        
        if verbose: print "Wykonuje funkcje " + self.function.__name__ + " (z argumentami" + str(self.args) + str(self.kwargs) + "):"  
            
        for j in range(self.times_to_exec):
            
            if verbose: print "po raz " + str(j), 
            result_raw = self.function(*self.args, **self.kwargs)
            if verbose: print "z wynikiem: " + str(result_raw)
            
            self.task_result.add_task_result(result_raw)
        return self.task_result
        
    def _get_str_about(self):
        return self.function.__name__ + " - " + str(self.times_to_exec) + " - " + str(self.args) + " - " + str(self.kwargs)

class TaskBucketResult(object):
    '''Container for results of tasks.'''
    def __init__(self, taskBucket, bucket_initialize_time=None):
        if bucket_initialize_time == None:
            bucket_initialize_time = datetime.datetime.now()
        self.taskBucket = taskBucket
        self.bucket_initialize_time = bucket_initialize_time
        self.bucket_result = []
        
    def add_bucket_result(self, task_result, task_execution_datetime=None):
        '''Adds results of task to bucket of task results.'''
        if task_execution_datetime == None:
            task_execution_datetime = datetime.datetime.now()
        
        self.bucket_result += [(task_result, task_execution_datetime)]
        
    def _get_str_bucket_result(self):
        '''Private function to help get_table_bucket_result'''
        results = [['#task', '#task_run', 'function / result']]  
        results[0].append('task time')
        for index1, elem1 in enumerate(self.bucket_result, 1):
            results.append([str(index1), '',str(elem1[0].task.function.__name__),elem1[1].strftime('%c')])
            
            for index2, elem2 in enumerate(elem1[0].task_result, 1):
                results.append(['', str(index2), str(elem2[0]), elem2[2].strftime('%c')])           
        return results
        
    def get_table_bucket_result(self):
        '''Prints results of bucket in pretty terminal table.'''
        table_data = self._get_str_bucket_result()
        table = terminaltables.SingleTable(table_data)        
        table.title = self.taskBucket.name + ' | ' + self.bucket_initialize_time.strftime('%c')       
        table.inner_row_border = True
        table.justify_columns = {0: 'right', 1: 'left', 2: 'center', 3: 'center'}
        # \n because terminaltables.table's output lacks it
        return "\n" + table.table

class TaskBucket(object):   
    '''Container for tasks to execute.'''  
    def __init__(self, name):
        self.bucket = []
        self.name = name
        
    def execute(self, settings_file=None, output=os.path.abspath(__file__), verbose = False):
        '''Executes bucket of tasks. Can take some time.'''
        if verbose: print 'Wykonuje zadanie: ' + self.name + '.'
        
        self.bucket_result = TaskBucketResult(self) 
        for i in self.bucket:
            self.bucket_result.add_bucket_result(i.execute_task())
        return self.bucket_result
        
    def add_task(self, func, times_to_exec=1, *args, **kwargs):
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
            
    def list_bucket(self):
        '''Lists bucket.'''
        return_str = '[ id - function name - times to execute - args - kwargs ]\n'
        
        for index, tsk in enumerate(self.bucket):
            return_str += "[ " + str(index) + " - " + tsk._get_str_about() + " ]\n"        
        # [:-1] = without \n
        return return_str[:-1]
        