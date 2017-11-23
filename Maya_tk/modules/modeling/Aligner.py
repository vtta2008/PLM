# -*-coding:utf-8 -*
"""

Script Name: Aligner.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It will make a simple UI which contains tools to align things including objects, components base on selection.

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA MODULES
# -------------------------------------------------------------------------------------------------------------

from maya import cmds
from functools import partial
import os

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
winID = 'ALigner'
winTitle = 'Objects Aligner'

def getIcon(icon):
    iconPth = os.path.join(os.getenv('PIPELINE_TOOL'), 'Maya_tk/icons')
    return os.path.join(iconPth, icon)

def createIconButton(icon, command=None):
    if command:
        cmds.iconTextButton(image1=getIcon(icon), w=50, h=50, c=command)
    else:
        cmds.iconTextButton(image1=getIcon(icon), w=50, h=50)

class Aligner(object):
    
    def __init__(self):
        super(Aligner, self).__init__()

        self.buildUI()

    def buildUI(self):

        if cmds.window(winID, q=True, exists=True):
            cmds.deleteUI(winID)

        cmds.window(winID, t=winTitle)
        mlo = cmds.columnLayout()

        # Add radio buttons for axis
        cmds.frameLayout(l='Choose an axis')

        cmds.gridLayout(nc=3, cw=50)
        cmds.radioCollection()
        self.xAxis = cmds.radioButton(l='x', select=True)
        self.yAxis = cmds.radioButton(l='y')
        self.zAxis = cmds.radioButton(l='z')

        createIconButton('XAxis.png', partial(self.onOptionClick, self.xAxis))
        createIconButton('YAxis.png', partial(self.onOptionClick, self.yAxis))
        createIconButton('ZAxis.png', partial(self.onOptionClick, self.zAxis))

        cmds.setParent(mlo)

        # Add radio buttons for mode
        cmds.frameLayout(l='Choose where to algin')

        cmds.rowLayout(nc=3)

        cmds.gridLayout(nc=3, cw=50)
        cmds.radioCollection()
        self.minMode = cmds.radioButton(l='Min')
        self.midMode = cmds.radioButton(l='Mid', select=True)
        self.maxMode = cmds.radioButton(l='Max')

        createIconButton('MinAxis.png', partial(self.onOptionClick, self.minMode))
        createIconButton('MidAxis.png', partial(self.onOptionClick, self.midMode))
        createIconButton('MaxAxis.png', partial(self.onOptionClick, self.maxMode))

        cmds.setParent(mlo)

        # Add apply button
        cmds.button(l='Align', c=self.onApplyClick, w=150, bgc=(.2,.5,.9))

        cmds.showWindow(winID)

        cmds.window(winID, e=True, resizeToFitChildren=True)

    def onOptionClick(self, opt, *args):

        cmds.radioButton(opt, e=True, select=True)

    def onApplyClick(self, *args):
        # Get the axis
        if cmds.radioButton(self.xAxis, q=True, select=True):
            axis = 'x'
        elif cmds.radioButton(self.yAxis, q=True, select=True):
            axis = 'y'
        else:
            axis = 'z'

        # Get the mode
        if cmds.radioButton(self.minMode, q=True, select=True):
            mode = 'min'
        elif cmds.radioButton(self.midMode, q=True, select=True):
            mode = 'mid'
        else:
            mode = 'max'

        # Call the algin function
        self.align(axis=axis, mode=mode)

    def align(self, nodes=None, axis='x', mode='mid', *args):
        # Default nodes to selection if not provided
        if not nodes:
            nodes = cmds.ls(sl=True)

        if not nodes:
            cmds.confirmDialog(t='Error', m='Nothing is selected', b='Ok')

        _nodes = []

        for node in nodes:
            if '.f[' in node:
                node = cmds.polyListComponentConversion(node, fromFace=True, toVertex=True)
            elif '.e[' in node:
                node = cmds.polyListComponentConversion(node, fromEdge=True, toVertex=True)

            cmds.select(node)
            node = cmds.ls(sl=True, fl=True)

            _nodes.extend(node)

        node = _nodes

        # Get the dimensions of our objects
        bboxes = {}
        if axis == 'x':
            start = 0
        elif axis == 'y':
            start = 1
        elif axis == 'z':
            start = 2
        else:
            cmds.confirmDialog(t='error', m='Unknown Axis', b='Ok')

        minMode = mode == 'min'
        maxMode = mode == 'max'
        midMode = mode == 'mid'

        values = []

        for node in nodes:
            if '.vtx[' in node:
                ws = cmds.xfrom(node, q=True, t=True, w=True)
                minValue = midValue = maxValue = ws[start]
            else:
                bbox = cmds.exactWorldBoundingBox(node)

                minValue = bbox[start]
                maxValue = bbox[start+3]
                midValue = (minValue+maxValue)/2

            bboxes[node] = (minValue, midValue, maxValue)

            if minMode:
                values.append(minValue)
            elif maxMode:
                values.append(maxValue)
            else:
                values.append(midValue)

        # Calculating the alignment point
        if minMode:
            target = min(values)
        elif maxMode:
            target = max(values)
        else:
            target = sum(values)/len(values)

        # Figure out the distance to the alignment point
        for node in nodes:
            bbox = bboxes[node]

            minValue, midValue, maxValue = bbox

            ws = cmds.xform(node, q=True, translation = True, ws=True)

            width = maxValue - minValue

            if minMode:
                distance = minValue - target
                ws[start] = (minValue - distance) + width/2
            elif maxMode:
                distance = target - maxValue
                ws[start] = (maxValue + distance) - width/2
            else:
                distance = target - midValue
                ws[start] = midValue + distance

        # Move objects to the target
        cmds.xform(node, translation=ws, ws=True)

def initialize():
    Aligner()

if __name__=="__main__":
    initialize()

# -------------------------------------------------------------------------------------------------------------
# END OF CODE
# -------------------------------------------------------------------------------------------------------------