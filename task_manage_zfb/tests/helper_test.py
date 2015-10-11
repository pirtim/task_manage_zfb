import os

test_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_files_gitignore')

worker_configfile_path = os.path.join(test_folder_path, '.zfb_config')
master_configfile_path = os.path.join(test_folder_path, '.zfb_config')
test_configfile_path = os.path.join(test_folder_path, '.conf_file')
normalfile_path = os.path.join(test_folder_path, '.normal_file')
emptyfile_path = os.path.join(test_folder_path, '.empty_file')

files_path = [worker_configfile_path, master_configfile_path, test_configfile_path, normalfile_path, emptyfile_path]

def delete_if_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
        
def clean_up():
    for path in files_path:
        delete_if_file(path)