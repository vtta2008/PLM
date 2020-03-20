# -*- coding: utf-8 -*-
"""

Script Name: BaseStorage.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    

"""
# -------------------------------------------------------------------------------------------------------------

from PLM.commons                            import DAMGDICT

class BaseStorage(DAMGDICT):

    Type                                    = 'DAMGSTORAGE'
    key                                     = 'BaseStorage'
    _name                                   = 'DAMG Storage'

    def __init__(self):
        super(BaseStorage, self).__init__()

    def register(self, obj):
        key                                 = obj.key

        if self.checkAttr('key', obj) and not self.isRegistered(obj):
            self.add(key, obj)


    def isRegistered(self, obj):

        if obj.key in self.keys():
            return True
        else:
            return False

    def deRegister(self, obj):
        key                                 = obj.key

        if self.checkAttr('key', obj) and self.isRegistered(obj):
            try:
                del self[key]
            except KeyError:
                self.pop(key, None)
            return True

    def checkAttr(self, attrName, obj):

        try:
            if attrName == 'key':
                obj.key
            elif attrName == 'Type':
                obj.Type
            else:
                obj._name
        except AttributeError:
            return False
        else:
            return True

    def setType(self, typeName, obj):
        if not self.checkAttr('Type', obj):
            obj.__setattr__('Type', typeName)
        return obj

    def setKey(self, obj):
        if not self.checkAttr('Key', obj):
            obj.__setattr__('key', obj.__class__.__name__)
        return obj

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/21/2020 - 2:44 AM
# © 2017 - 2019 DAMGteam. All rights reserved