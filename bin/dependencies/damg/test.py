# -*- coding: utf-8 -*-
"""

Script Name: analogClock.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from damg import DAMGLIST, DAMGDICT, DAMGERROR, DAMG, DAMGWORKER, DAMGTHREAD, DAMGTHREADPOOL, DamgWorkerSignals

o = DAMG()
a = DAMG()
b = DAMG()
c = DAMG()
l = DAMGLIST()
d = DAMGDICT()
e = DAMGERROR()
w = DAMGWORKER()
t = DAMGTHREAD("my_task")
p = DAMGTHREADPOOL()
s = DamgWorkerSignals()

def print_test(obj):
    if obj.Type == 'DAMGDICT' or obj.Type == 'DAMGLIST':
        print("object: {0} \n type: {1}".format(obj.data, obj.Type))
    else:
        print("object: {0} \n type: {1}".format(obj, obj.Type))

def check_count(obj):
    print("object: {0} - count: {1}".format(obj.name, obj.count))

for obj in [o, a, b, c, d, l, d, e, w, t, p, s, ]:
    # print_test(obj)
    # check_count(obj)
    print(obj)



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/10/2019 - 11:25 PM
# © 2017 - 2018 DAMGteam. All rights reserved