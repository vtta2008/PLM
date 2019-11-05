# -*- coding: utf-8 -*-
"""

Script Name: test.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

class my_decorator(object):

    def __init__(self, f):
        # print("inside my_decorator.__init__()")
        f() # Prove that function definition has completed

    def __call__(self):
        if isinstance(self, (object)):
            return True
        else:
            return False

@my_decorator
def aFunction(txt='aaaa'):
    print(txt)

# print("Finished decorating aFunction()")

aFunction()

from cores.Version import version

ver = version()
print(str(ver), type(str(ver)), type(ver))

print(ver.mro(ver))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 6/11/2019 - 1:38 AM
# © 2017 - 2018 DAMGteam. All rights reserved