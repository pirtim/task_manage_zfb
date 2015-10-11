from errors import *
from config import *
import master_bucket as mb
import worker_bucket as wb

import os

def _on_master(folder_path=''):
    zfb_file_name = '.zfb_config'
    return not WorkerConfig.is_config_file(os.path.join(folder_path, zfb_file_name))

def makeBucket(name, folder_path=''):
    if _on_master(folder_path):
        return mb.TaskBucket(name)
    else:
        return wb.TaskBucket(name)

if __name__ == "__main__":
    def tests():
        '''Funkcja zawierajaca testy'''
        def moje_obliczenia1(a, b):
            return a + b
            
        def moje_obliczenia2(a, b):
            return a * b
            
        def moje_obliczenia3():
            return uuid.uuid1()
            
        def return_tuple():
            return (random.randint(1, 10), [random.randint(1, 10)])
            
        buck = makeBucket(name="Moje obliczenia")
        
        buck.add_task(moje_obliczenia1, 1, *(1, 5))
        buck.add_task(moje_obliczenia2, 1, *(4, 5))
        buck.add_task(moje_obliczenia3, 1)
        buck.add_task(return_tuple, 1)
        
        my_results = buck.execute()
        
        print my_results.get_table_bucket_result()
    
    tests()
    # cokolwiek
    pass
    