# -*- coding: utf-8 -*-
from __future__ import division

from fabric.api import run, env, local, settings, abort, execute
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project
from fabric.decorators import runs_once
from fabric.context_managers import hide

import terminaltables
import os
import datetime
import uuid
import random
import time
import logging

from errors import TaskNotFoundError
from worker_bucket import TaskBucketResult, TaskResult, TaskBucket, Task

class MasterTaskResult(TaskResult):
    pass

class MasterTaskBucketResult(TaskBucketResult):
    def _get_tablestr_bucket_result(self):
        '''Private function to help get_table_bucket_result'''
        results = [['#task', '#task_run', 'function / result']]
        results[0].append('task time')
        for index1, result_bucket in enumerate(self, 1):
            results.append([str(index1), '',str(result_bucket.task_rst.task.function.__name__),result_bucket.time.strftime('%c')])

            for index2, result_task in enumerate(result_bucket[0], 1):
                results.append(['', str(index2), str(result_task.hex), result_task.time.strftime('%c')])
        return results

    def get_table_bucket_result(self):
        '''Prints results of bucket in pretty terminal table.'''
        table_data = self._get_tablestr_bucket_result()
        table = terminaltables.SingleTable(table_data)
        table.title = self.taskBucket.name + ' | ' + self.bucket_initialize_time.strftime('%c')
        table.inner_row_border = True
        table.justify_columns = {0: 'right', 1: 'left', 2: 'center', 3: 'center'}
        # \n because terminaltables.table's output lacks it
        return "\n" + table.table

class MasterTask(Task):
    def execute_task(self, ClsResult = MasterTaskResult):
        return Task.execute_task(self, ClsResult)

class MasterTaskBucket(TaskBucket):
    '''Container for tasks to execute on master.'''

    def execute(self, settings_file=None, output=os.path.abspath(__file__), ClsResult = MasterTaskBucketResult):
        '''Executes bucket of tasks. Can take some time.'''
        return TaskBucket.execute(self, settings_file, output, ClsResult)
