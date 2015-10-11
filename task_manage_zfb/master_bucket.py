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

class TaskBucket(object):   
    '''Container for tasks to execute.'''  
    def __init__(self, name):
        self.bucket = []
        self.name = name