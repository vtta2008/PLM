# -*-coding:utf-8 -*
"""

Script Name: Randomizer.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It will make an simple UI to move objects around randomly base on selection.

"""

# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds
import random

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
winID = 'Randomizer'
winTitle = 'Objects Randomizer'

class Randomizer(object):

    def __init__(self):
        super(Randomizer, self).__init__()

        self.buildUI()

    def buildUI(self):

        if cmds.window(winID, q=True, exists=True):
            cmds.deleteUI(winID)

        cmds.window(winID, t=winTitle)

        mlo = cmds.columnLayout()
        cmds.frameLayout(label='Choose an object type')

        cmds.columnLayout()
        self.objType = cmds.radioCollection()
        cmds.radioButton(label='Sphere')
        cmds.radioButton(label='Cube', select=True)
        cmds.radioButton(label='Cone')
        cmds.radioButton(label='Cylinder')

        self.numOfObjs = cmds.intField(value=3)

        cmds.setParent(mlo)

        frame = cmds.frameLayout("Choose your max range")
        cmds.gridLayout(nc=2, cellWidth=100)

        for axis in 'xyz':
            cmds.text(label='%s axis' % axis)
            cmds.floatField('%sAxisField' % axis, value=random.uniform(0,10))

        cmds.setParent(frame)
        cmds.rowLayout(nc=2)

        cmds.radioCollection("randomMode")
        cmds.radioButton(label='Absolute', select=True)
        cmds.radioButton(label='Relative')

        cmds.setParent(mlo)
        cmds.rowLayout(nc=2)
        cmds.button(l="Create", c=self.onCreateClick)
        cmds.button(l="Randomize", c=self.onRandomClick)

        cmds.showWindow(winID)

    def onCreateClick(self, *args):
        radio = cmds.radioCollection(self.objType, q=True, select=True)
        mode = cmds.radioButton(radio, query=True, label=True)

        numObjects = cmds.intField(self.numOfObjs, q=True, value=True)

        self.createObjects(mode, numObjects)

        self.onRandomClick()

    def onRandomClick(self, *args):
        radio = cmds.radioCollection(self.objType, q=True, select=True)
        mode = cmds.radioButton(radio, query=True, label=True)

        for axis in 'xyz':
            val = cmds.floatField('%sAxisField' % axis, q=True, v=True)
            self.randomize(minValue=val*-1, maxValue=val, mode=mode, axes=axis)

    def createObjects(self, mode, numObjects, *args):
        """
        This creates objects. Support Cubes, Spheres, Cylinders and Cones
        :param mode: To create objects
        :param numObjects: Number of objects will be created
        :return: a list of created objects
        """

        objList = []

        for n in range(numObjects):
            if mode == 'Cube':
                obj = cmds.polyCube()
            elif mode == 'Sphere':
                obj = cmds.polySphere()
            elif mode == 'Cone':
                obj = cmds.polyCone()
            elif mode == 'Cylinder':
                obj = cmds.polyCylinder()
            else:
                cmds.error("I dont know what to create")

            objList.append(obj[0])

        cmds.select(objList)

    def randomize(self, objList=None, minValue=0, maxValue=50, axes='xyz', mode='Absolute', *args):

        if objList is None:
            objList = cmds.ls(sl=True)

        for obj in objList:
            for axis in axes:
                current = 0
                if mode == 'Relative':
                    current = cmds.getAttr(obj+'.t%s' % axis)

                val = current + random.uniform(minValue, maxValue)

                cmds.setAttr(obj+'.t%s' % axis, val)

def initialize():
    Randomizer()

if __name__=="__main__":
    initialize()

# -------------------------------------------------------------------------------------------------------------
# END OF CODE
# -------------------------------------------------------------------------------------------------------------