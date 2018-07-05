# -*- coding: utf-8 -*-
"""

Script Name: _attr.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------

variable = dict(

    varCfg = ['docs', 'keys', 'metadata', 'path', 'pref'],

    varLib = ['color', 'format', 'classAttr', 'nodeGraph'],

    varCustom = ['exeption', 'event', 'channel', 'sender', 'receiver', 'setting', 'property', 'slot', 'thread']

),

defineMtd = dict(
    metadata=['id', 'name', 'email', 'author', 'sysInfo', 'webstie', 'contact'],
),

sysInfo = dict(
    log = ['logtype', 'logContent', 'datetimestamp'],
),

datatype = dict(

    value = ['int', 'float', 'mess', ],
    metadata = ['attr', 'tag', 'unix', 'name', 'id'],
    data = ['list', 'dict', 'path', 'setting', ],
    technic = ['signal', 'slot', 'event'],

),

attrLst = dict(

    ui=['id', 'unix', 'sysID','metadata', 'uiname', 'className', 'childLst', 'funcLst', 'attrList', 'settingLst', 'eventLst',
        'signalLst', 'slotLst', 'propertyLst'],

    uisetting=['uiName', 'className', 'posx', 'posy', 'width', 'height', 'attrname', 'attrvalue', 'attrvaluetype'],

    obj=['id', 'unix', 'sysID', 'metaobj', 'objname', 'className', 'childLst', 'funcLst', 'attrList', 'settingLst', 'eventLst',
             'signalLst', 'slotLst', 'propertyLst'],

    objsetting=['objName', 'className', 'datavalue', 'attrname', 'funcvalue', 'valuetype', 'signalid', 'slotid',
                'property'],
),


dataStructer = dict(

    curUser = ['username', 'token', 'data'],

    format = ['typeformat', 'formatAttr', 'value', 'typeValue'],

    config = ['id', 'value', 'varType'],

),


# Nodegraph definition

scene = dict(

    metadata = ['id', 'unixID', 'type', 'rect', 'zoom', 'pos', 'nodeLst', 'knobLst', 'edgeLst', 'save', 'merge', 'setting'],
    realtime = ['grid', 'layout' , 'save', 'load', 'new', 'merge'],
    func = [],
    uiElement = [],
),

node = dict(

    metadata = ['id', 'unixID', 'type', 'property', 'knobLst', 'inputLst', 'outputLst', 'knobLst', 'signalLst', 'attrLst', ],
    realtime = ['curInputLst', 'curOutputLst', 'curRect', 'addNewAttr', 'pos', 'condition', 'setting', 'signal'],
),

knob = dict(

    metadata = ['id', 'unixID', 'type', 'property'],
    realtime = ['stage', 'status', 'event', 'signal', 'slot', 'setting', 'history'],
    func = ['create', 'disconnet', 'connect', 'replace', 'add']

),

edgeAttrLst = dict( edge = ['id', 'unixID', 'type', 'start', 'end', 'middle', 'setting', 'history', 'behave', 'disconnect', 'connect', 'event', 'signal', 'slot'], )

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/06/2018 - 4:02 AM
# © 2017 - 2018 DAMGteam. All rights reserved