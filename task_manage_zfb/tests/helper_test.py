import os
import logging
import subprocess

test_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files_gitignore')

worker_configfile_path = os.path.join(test_folder_path, '.zfb_config')
master_configfile_path = os.path.join(test_folder_path, '.zfb_config')
test_configfile_path = os.path.join(test_folder_path, '.conf_file')
normalfile_path = os.path.join(test_folder_path, '.normal_file')
emptyfile_path = os.path.join(test_folder_path, '.empty_file')

loggerfile_path = os.path.join(test_folder_path, 'main.log')

files_path = [worker_configfile_path, master_configfile_path, test_configfile_path, normalfile_path, emptyfile_path]

def delete_if_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
        
def help_set_up():
    if not os.path.isdir(test_folder_path):
        os.mkdir(test_folder_path) 
    with open(normalfile_path, 'w') as normalfile:
        normalfile.write("test")
    with open(emptyfile_path, 'w') as emptyfile:
        emptyfile.write("")
    
def help_tear_down():
    for path in files_path:
        delete_if_file(path)
    # os.rmdir(test_folder_path)
    
def id_fun(x):
    return x
    
def run_host_name():
    return subprocess.check_output(["hostname"]).strip()
    
local_hostname = subprocess.check_output(["hostname"]).strip()
    