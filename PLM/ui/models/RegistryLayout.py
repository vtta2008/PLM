# -*- coding: utf-8 -*-
"""

Script Name: RegistryLayout.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

import datetime, time
from PLM import DAMGDICT, DAMGLIST, DAMG
from PLM import layoutTypes


class InspectLayout(DAMG):

    key                     = 'InspectLayout'
    layoutTypes             = DAMGLIST()
    layoutKeys              = DAMGLIST()

    def __init__(self, parent=None):
        super(InspectLayout, self).__init__(parent)

        self.layoutTypes.appendList(layoutTypes)

    def doInspection(self, layout):
        self.layoutTypes.append(layout.Type)
        self.layoutKeys.append(layout.key)
        return layout

    def checkType(self, layout):
        if not self.haveType(layout):
            try:
                layout.show()
            except AttributeError:
                layoutType  = 'Object'
            else:
                layoutType  = 'UI'
            layout.__setattr__('Type', layoutType)

        return self.checkKey(layout)

    def checkKey(self, layout):
        if not self.haveKey(layout):
            key = layout.__class__.__name__
            layout.__setattr__('key', key)

        return layout

    def haveType(self, layout):
        try:
            layout.Type
        except AttributeError:
            return False
        else:
            return True

    def haveKey(self, layout):
        try:
            layout.key
        except KeyError:
            return False
        else:
            return True



class RegistryLayout(DAMGDICT):

    awaitingSlots           = DAMGLIST()
    layout_names            = DAMGLIST()
    layout_ids              = DAMGLIST()
    layout_datetimes        = DAMGLIST()
    layout_keys             = DAMGLIST()

    def __init__(self):
        super(RegistryLayout, self).__init__(self)

        self.inspect        = InspectLayout(self)

    def regisLayout(self, layout):

        ui                  = self.inspect.doInspection(layout)
        key                 = ui.key

        if self.isLayout(ui):
            if self.isAwaitingSlot(ui):
                self.awaitingSlots.remove(key)
                self.doRegister(ui)
            else:
                if not self.isRegistered(ui):
                    self.doRegister(ui)
                else:
                    print("Already registered: {0}".format(key))
                    return False

    def isAwaitingSlot(self, layout):
        key = layout.key
        if key in self.awaitingSlots:
            return True
        else:
            return False

    def doRegister(self, layout):
        key = layout.key

        self.layout_names.append(layout.name)
        self.layout_ids.append(id(layout))
        self.layout_datetimes.append(str(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S|%d.%m.%Y')))
        self.layout_keys.append(layout.key)

        self[key] = layout
        return True

    def deRegister(self, layout):
        key = layout.key
        index = self.layout_names.index(layout.name)

        if self.isRegistered(layout):
            self.awaitingSlots.append(key)
            try:
                del self[key]
            except KeyError:
                self.pop(key, None)
            self.layout_names.remove(self.layout_names[index])
            self.layout_ids.remove(self.layout_ids[index])
            self.layout_datetimes.remove(self.layout_datetimes[index])
            return True
        else:
            return False

    def isRegistered(self, layout):
        key = layout.key
        if key in self.keys():
            return True
        else:
            return False

    def isLayout(self, layout):
        if layout.Type in self.inspect.layoutTypes:
            return True
        else:
            return False



# -------------------------------------------------------------------------------------------------------------
# Created by panda on 8/11/2019 - 4:18 PM
# © 2017 - 2018 DAMGteam. All rights reserved