# -*- coding: utf-8 -*-
"""

Script Name: __init__.py.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
import pprint
import sys
import time
from threading import Thread, current_thread

import os

pprint.pprint(os.getenv('PATH'))

C:\Users\dapco\AppData\Roaming\Python\Python37\Scripts

def do_something_with_exception():
    pprint.pprint(sys.exc_info())
    exc_type, exc_value = sys.exc_info()[:2]
    print('Handling {0} exception with message "{1}" in {2}'.format(exc_type.__name__, exc_value, current_thread().name))



def cause_exception(delay):
    time.sleep(delay)
    raise RuntimeError('This is the error message')



def thread_target(delay):
    try:
        cause_exception(delay)
    except:
        do_something_with_exception()




def main():

    threads = [Thread(target=thread_target, args=(0.3,)), Thread(target=thread_target, args=(0.1,)), ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()





if __name__ == '__main__':
    sys.exit(main())

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/16/2020 - 2:17 AM
# © 2017 - 2019 DAMGteam. All rights reserved