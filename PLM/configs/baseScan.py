# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os

from bin.damg import DAMGLIST, DAMG


class BaseScan(DAMG):

    key                 = 'AutoScanner'

    _missing            = DAMGLIST()
    _findout            = DAMGLIST()

    alldirs             = None
    allpths             = None


    def __init__(self, parent=None):
        super(BaseScan, self).__init__(parent)


    def scanAndFix(self):
        self.scan(self.alldirs, True)
        if 'Dir' in self.key:
            return print('finish scanning directories')
        elif 'Pth' in self.key:
            return print('finish scanning paths')
        else:
            return print('finish scanning')


    def scan(self, dirs=[], fix=False):
        for d in dirs:
            if not os.path.exists(d):
                if fix:
                    return self.fixDir()
                else:
                    self._missing.append(d)
                    print('Detect path not exists: {0}'.format(d.replace('\\', '/')))

        self.update()

    def fixDir(self):
        for d in self.missing:
            self.makeDir(d)

    def makeDir(self, pth, mode=0o770):

        if not pth or os.path.exists(pth):
            return []

        (head, tail) = os.path.split(pth)
        res = self.makeDir(head, mode)
        try:
            original_umask = os.umask(0)
            os.makedirs(pth, mode)
        except:
            os.chmod(pth, mode)
        finally:
            os.umask(original_umask)
        res += [pth]

    def clear(self):
        return self._missing.clear(), self._findout.clear()

    @property
    def missing(self):
        return self._missing

    @missing.setter
    def missing(self, val):
        self._missing   = val

    @property
    def findout(self):
        return self._findout

    @findout.setter
    def findout(self, val):
        self._findout   = val



# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
