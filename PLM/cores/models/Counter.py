# -*- coding: utf-8 -*-
"""

Script Name: Counting.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# PLM
from PLM.commons.Core                       import Timer


class Counter(Timer):

    key                                     = 'Counting'
    printCounter                            = False
    _isCounting                             = False
    _counter                                = 0

    def __init__(self, countLimited=0, interval=10000):
        super(Counter, self).__init__()

        self._interval                      = interval
        self._countLimited                  = countLimited
        self.setInterval(self._interval)

    def begin(self):
        if self.printCounter:
            print("Start counting")

        self.timeout.connect(self.counting)
        self.start(1000)
        self._isCounting                    = True

    def counting(self):
        if self._counter == 0:
            self._counter += 1
        elif self._counter == self._countLimited:
            self.finish()
        else:
            self._counter += 1

        if self.printCounter:
            print(self._counter)

    def finish(self):
        if self.printCounter:
            print("Stop counting")
        self.stop()
        self._isCounting                    = False

    def setStartCounter(self, val):
        self._counter                       = val

    def setCountLimited(self, val):
        if not self._countLimited == val:
            if self.printCounter:
                print('countLimited is set to: {0}'.format(val))
            self._countLimited = val

        return self._countLimited

    def setPrintCounter(self, bool):
        if bool:
            if not self.printCounter:
                self.printCounter = bool
        else:
            if self.printCounter:
                print('printCounter is set to: {0}'.format(bool))
                self.printCounter = bool
            else:
                print('printCounter is set to: {0}'.format(bool))

        return self.printCounter

    @property
    def counter(self):
        return self._counter

    @property
    def countLimited(self):
        return self._countLimited

    @property
    def isCounting(self):
        return self._isCounting

    @counter.setter
    def counter(self, val):
        self._counter                       = val

    @countLimited.setter
    def countLimited(self, val):
        self._countLimited                  = val

    @isCounting.setter
    def isCounting(self, val):
        self._isCounting                    = val


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/21/2020 - 1:48 AM
# © 2017 - 2019 DAMGteam. All rights reserved