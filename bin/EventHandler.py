# -*- coding: utf-8 -*-
"""

Script Name: EventHandler.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

class EventHandler(object):

    def __init__(self, sender):

        self.callbacks = []
        self.sender = sender
        self.blocked = False

    def __call__(self, *args, **kwargs):
        if not self.blocked:
            return [callback(self.sender, *args, **kwargs) for callback in self.callbacks]
        return []

    def __iadd__(self, callback):
        self.add(callback)
        return self

    def __isub__(self, callback):
        self.remove(callback)
        return self

    def __len__(self):
        return len(self.callbacks)

    def __getitem__(self, index):
        return self.callbacks[index]

    def __setitem__(self, index, value):
        self.callbacks[index] = value

    def __delitem__(self, index):
        del self.callbacks[index]

    def blockSignals(self, block):
        self.blocked = block

    def add(self, callback):
        if not callable(callback):
            raise TypeError("callback must be callable")
        self.callbacks.append(callback)

    def remove(self, callback):
        self.callbacks.remove(callback)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 21/07/2018 - 11:37 PM
# © 2017 - 2018 DAMGteam. All rights reserved