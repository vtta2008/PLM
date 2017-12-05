# -*-coding:utf-8 -*
"""

Script Name: ToolBoxI.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It will load an UI which can rename and add attributes to object inside Maya.

"""

import logging
import sys

from maya import cmds

# -------------------------------------------------------------------------------------------------------------
# MAKE MAYA UNDERSTAND QT UI AS MAYA WINDOW,  FIX VERSION CONVENTION
# -------------------------------------------------------------------------------------------------------------
# We can configure the current level to make it disable certain logs when we don't want it.
logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


# -------------------------------------------------------------------------------------------------------------
# CHECK THE CORRECT BINDING THAT BE USING UNDER QT.PY
# -------------------------------------------------------------------------------------------------------------
# While Qt.py lets us abstract the actual Qt library, there are a few things it cannot do yet
# and a few support libraries we need that we have to import manually.
# if Qt.__binding__=='PySide':
#     logger.debug('Using PySide with shiboken')
#     from shiboken import wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import Signal
# elif Qt.__binding__.startswith('PyQt'):
#     logger.debug('Using PyQt with sip')
#     from sip import wrapinstance as wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import pyqtSignal as Signal
# else:
#     logger.debug('Using PySide2 with shiboken2')
#     from shiboken2 import wrapInstance
#     from Maya_tk.plugins.Qt.QtCore import Signal

class DAMGtoolBoxI(object):
    def __init__(self):
        if cmds.window('DAMGcommonToolMainUI', exists=True):
            cmds.deleteUI('DAMGcommonToolMainUI')

        cw2 = [(1, 5), (2, 100), (3, 250), (4, 5)]
        cw3 = [(1, 5), (2, 105), (3, 5), (4, 130), (5, 5), (6, 105), (7, 5)]

        def makeDistanceForRowcolumn(height, times):
            i = 0
            for i in range(times):
                cmds.text(l="", h=height)
                i += 1

        cmds.window('DAMGcommonToolMainUI', t="DAMG Tool Box I", rtf=True)
        # menu
        cmds.columnLayout()
        cmds.menuBarLayout()
        cmds.menu(label='About')
        cmds.menuItem(d=True)
        cmds.menuItem(label='About DAMG Tool Box I')
        tabControl = cmds.tabLayout()
        # renamer tab
        t1 = cmds.columnLayout()
        cmds.separator(style='in', w=360, h=8)
        # copy and replace
        cmds.rowColumnLayout(nc=4, cw=cw2)
        makeDistanceForRowcolumn(2, 4)
        cmds.text(l="")
        cmds.text(l="Search", align='center')
        self.tfSearch = cmds.textField('tfSearch', tx="")
        cmds.text(l="")
        makeDistanceForRowcolumn(2, 4)
        cmds.text(l="")
        cmds.text(l="Replace", align='center')
        self.tfReplace = cmds.textField('tfReplace', tx="")
        cmds.text(l="")
        cmds.setParent('..')
        cmds.text(l="", h=8)
        cmds.rowColumnLayout(nc=5, cw=[(1, 5), (2, 172.5), (3, 5), (4, 172.5), (5, 5)])
        cmds.text(l="")
        cmds.button(l="Search And Select", c=self.searchAndSelect)
        cmds.text(l="")
        cmds.button(l="Search And Replace", c=self.searchAndReplace)
        cmds.text(l="")
        cmds.setParent('..')
        cmds.text(l="", h=5)
        cmds.separator(style="in", w=360, h=8)
        cmds.text(l="", h=5)
        # number and padding setting
        cmds.rowColumnLayout(nc=3, cw=[(1, 200), (2, 100), (3, 60)])
        cmds.text(l="", w=200)
        cmds.text(l="Number", w=100)
        self.ifNumber = cmds.intField('ifNumber', v=0, w=60, min=0)
        cmds.setParent('..')
        cmds.rowColumnLayout(nc=3, cw=[(1, 200), (2, 100), (3, 60)])
        cmds.button(l="Auto Rename By Type", align='center', c=self.autoRename)
        cmds.text(l="Padding", w=100)
        self.ifPadding = cmds.intField('ifPadding', v=0, w=60, min=0)
        cmds.text(l="", w=200, h=8)
        cmds.separator(style='in', w=160)
        cmds.text(l="", w=60, h=8)
        cmds.setParent('..')
        # rename with prefix and suffix, number and padding
        cmds.rowColumnLayout(nc=7, cw=cw3)
        cmds.text(l="", w=5)
        cmds.text(l="Prefix", align='center', w=105)
        cmds.text(l="", w=5)
        cmds.text(l="Rename", align='center', w=130)
        cmds.text(l="", w=5)
        cmds.text(l="Suffix", align='center', w=105)
        cmds.text(l="", w=5)
        cmds.setParent('..')
        cmds.text(l="", h=2)
        cmds.rowColumnLayout(nc=7, cw=cw3)
        cmds.text(l="", w=5)
        self.tfPrefix = cmds.textField('tfPrefix', tx="", w=105)
        cmds.text(l="", w=5)
        self.tfRename = cmds.textField('tfRename', tx="", w=130)
        cmds.text(l="", w=5)
        self.tfSuffix = cmds.textField('tfSuffix', tx="", w=105)
        cmds.text(l="", w=5)
        cmds.setParent('..')
        cmds.text(l="", h=2)
        cmds.rowColumnLayout(nc=7, cw=cw3)
        cmds.text(l="", w=5)
        cmds.button('button_prefix', l="Add Prefix", w=105, c=self.addPrefix)
        cmds.text(l="", w=5)
        cmds.button('button_rename', l="Rename", w=130, c=self.doRename)
        cmds.text(l="", w=5)
        cmds.button('button_suffix', l="Add Suffix", w=105, c=self.addSuffix)
        cmds.text(l="", w=5)
        cmds.setParent('..')
        cmds.text(l="", h=2)
        cmds.separator(style="in", w=360, h=8)
        # add attribute tab
        cmds.setParent(tabControl)
        t2 = cmds.columnLayout()
        cmds.separator(style='in', w=360, h=8)
        # long name and short name
        cmds.rowColumnLayout(nc=4, cw=[(1, 30), (2, 100), (3, 200), (4, 30)])
        cmds.text(l="")
        cmds.text(l="Long Name  ", align='center')
        cmds.textField('longNameAA', text="")
        makeDistanceForRowcolumn(4, 2)
        cmds.text(l="Short Name  ", align='center')
        cmds.textField('shortNameAA', text="")
        cmds.text(l="")
        cmds.setParent('..')
        cmds.text(l="", h=5)
        cmds.separator(w=360, style="in")
        cmds.text(l="", h=5)
        # value setting: min, max, default, float or boolean
        cmds.rowColumnLayout(nc=4, cw=[(1, 90), (2, 90), (3, 90), (4, 90)])
        cmds.text(l="Min")
        cmds.text(l="Default")
        cmds.text(l="Max")
        cmds.text(l="F/B")
        makeDistanceForRowcolumn(5, 4)
        cmds.intField('minIntAA', v=-360)
        cmds.intField('defIntAA', v=0)
        cmds.intField('maxIntAA', v=360)
        cmds.optionMenu('ForBAA')
        cmds.menuItem(l="Float")
        cmds.menuItem(l="Boolean")
        cmds.setParent('..')
        cmds.separator(style="in", w=360, h=5)
        cmds.text(l="", h=5)
        # add attribute button
        cmds.rowColumnLayout(nc=3, cw=[(1, 100), (2, 160), (3, 100)])
        cmds.text(l="")
        cmds.button(l="Add Attribute", c=self.addAttribute)
        makeDistanceForRowcolumn(5, 4)
        cmds.setParent('..')
        cmds.separator(style="in", w=360, h=5)
        # attribute presets
        cmds.rowColumnLayout(nc=5, cw=[(1, 30), (2, 147.5), (3, 5), (4, 147.5), (5, 30)])
        makeDistanceForRowcolumn(5, 5)
        cmds.text(l="")
        cmds.button(l="Left hand", c=self.leftHandPreset)
        cmds.text(l="")
        cmds.button(l="Right hand", c=self.rightHandPreset)
        cmds.text(l="")
        makeDistanceForRowcolumn(5, 5)
        cmds.text(l="")
        cmds.button(l="Left foot", c=self.leftFootPreset)
        cmds.text(l="")
        cmds.button(l="Right foot", c=self.rightFootPreset)
        cmds.text(l="")
        makeDistanceForRowcolumn(5, 5)
        cmds.setParent('..')
        cmds.separator(style="in", w=360, h=5)
        cmds.setParent(tabControl)

        cmds.tabLayout(tabControl, edit=True, tabLabel=((t1, 'Renamer'), (t2, 'Add Attribute')))
        cmds.showWindow('DAMGcommonToolMainUI')

    def doRenameShapes(self):
        objSelect = cmds.ls(sl=True)

        for i in range(len(objSelect)):
            typeCheck = cmds.objectType(objSelect[i])
            if (typeCheck == 'transform'):
                objShapes = cmds.listRelatives(objSelect[i], f=True)
                if (len(objShapes) == 1):
                    nodeCheck = cmds.objectType(objShapes[0])
                    if (nodeCheck == 'transform'):
                        break
                    else:
                        newShapeName = objSelect[i] + "Shape"
                        cmds.rename(objShapes[0], newShapeName)
                elif (len(objShapes) > 1):
                    node = 0
                    for node in range(len(objShapes)):
                        nodeCheck = cmds.objectType(objShapes[node])
                        if (nodeCheck == 'transform'):
                            break
                        else:
                            newShapeName = objSelect[i] + "_" + str(node + 1) + "Shape"
                            cmds.rename(objShapes[node], newShapeName)
                        node += 1
            else:
                break
            i += 1

    def autoRename(self, *args):
        objSelect = cmds.ls(sl=True)
        suffixes = {
            "mesh": "geo",
            "joint": "joint",
            "camera": None,
            "nurbsCurve": "nurbs",
            "parentConstraint": "parCons"
        }
        suffixes_default = "group"
        if (objSelect == []):
            objSelect = cmds.ls(dag=True, long=True)
            objSelect.sort(key=len, reverse=True)

        for obj in objSelect:
            shortName = obj.split("|")[-1]
            children = cmds.listRelatives(obj, c=True, f=True) or []
            if len(children) >= 1:
                child = children[0]
                objType = cmds.objectType(child)
            else:
                objType = cmds.objectType(obj)

            if "Light" in objType:
                suffix = "light"
            else:
                suffix = suffixes.get(objType, suffixes_default)
                if not suffix:
                    continue
            if obj.endswith(suffix):
                continue
            newName = shortName + "_" + suffix
            cmds.rename(obj, newName)
            cmds.select(newName, r=True)
            self.doRenameShapes()

    def doRename(self, *args):
        rename = cmds.textField('tfRename', q=True, tx=True)
        objSelect = cmds.ls(sl=True)
        if (rename == "") or (objSelect == []):
            if (rename == ""):
                message = 'Rename field entry is blank!'
            elif (objSelect == []):
                message = 'You select nothing'
            cmds.confirmDialog(t='Warning', m=message, b="Ok")
            cmds.warning(message)
            sys.exit()
        else:
            number = cmds.intField('ifNumber', q=True, value=True)
            padding = cmds.intField('ifPadding', q=True, value=True)
            if (len(objSelect) == 1):
                if (number == 0):
                    newName = rename
                else:
                    newName = rename + str(number)
                cmds.rename(objSelect[0], newName)
                self.doRenameShapes()
            elif (len(objSelect) > 1):
                if (number == 0):
                    if (padding == 0):
                        i = 0
                        for i in range(len(objSelect)):
                            newName = rename + str(i + 1)
                            cmds.rename(objSelect[i], newName)
                            i += 1
                        self.doRenameShapes()
                    else:
                        i = 0
                        for i in range(len(objSelect)):
                            padNum = str(number + padding * i)
                            cmds.rename(objSelect[i], rename + padNum)
                            i += 1
                        self.doRenameShapes()
                else:
                    if (padding == 0):
                        i = 0
                        for i in range(len(objSelect)):
                            newName = rename + str(number + i)
                            cmds.rename(objSelect[i], newName)
                            i += 1
                        self.doRenameShapes()
                    else:
                        i = 0
                        for i in range(len(objSelect)):
                            padNum = str(number + (padding * i))
                            newName = rename + padNum
                            cmds.rename(objSelect[i], newName)
                            i += 1
                        self.doRenameShapes()

    def addPrefix(self, *args):
        prefix = cmds.textField('tfPrefix', q=True, tx=True)
        objSelect = cmds.ls(sl=True) or []
        if (prefix == "") or (objSelect == []):
            if (prefix == ""):
                message = 'Prefix field entry is blank!'
            elif (objSelect == []):
                message = 'You select nothing'
            cmds.confirmDialog(t='Warning', m=message, b="Ok")
            cmds.warning(message)
            sys.exit()
        else:
            i = 0
            for i in range(len(objSelect)):
                newName = prefix + objSelect[i]
                cmds.rename(objSelect[i], newName)
                i += 1
            self.doRenameShapes()

    def addSuffix(self, *args):
        suffix = cmds.textField('tfSuffix', q=True, tx=True)
        objSelect = cmds.ls(sl=True)
        if (suffix == "") or (objSelect == []):
            if (suffix == ""):
                message = 'Suffix field entry is blank!'
            elif (objSelect == []):
                message = 'You select nothing'
            cmds.confirmDialog(t='Warning', m=message, b="Ok")
            cmds.warning(message)
            sys.exit()
        else:
            i = 0
            for i in range(len(objSelect)):
                newName = objSelect[i] + suffix
                cmds.rename(objSelect[i], newName)
                i += 1
            self.doRenameShapes()

    def searchAndSelect(self, *args):
        search = cmds.textField('tfSearch', q=True, tx=True)
        if (search == ""):
            cmds.confirmDialog(t='Warning', m="Search field entry is blank!", b="Ok")
            cmds.warning("Search field entry is blank!")
            sys.exit()
        else:
            objMatch = []
            objSelect = cmds.ls(dag=True, l=True)
            objSelect.sort(key=len, reverse=True)
            for i in objSelect:
                name = i.split("|")[-1]
                if search in name:
                    objMatch.append(name)
            cmds.select(objMatch, r=True)

    def searchAndReplace(self, *args):
        search = cmds.textField('tfSearch', q=True, tx=True)
        replace = cmds.textField('tfReplace', q=True, tx=True)
        objSelect = cmds.ls(sl=True)
        if (search == "") or (replace == "") or (objSelect == []):
            if (search == ""):
                message = "Search field entry is blank!"
            elif (replace == ""):
                message = 'Replace field entry is blank!'
            elif (objSelect == []):
                message = 'You select nothing'
            else:
                message = ''
            cmds.confirmDialog(t='Warning', m=message, b="Ok")
            cmds.warning(message)
            sys.exit()
        else:
            objMatch = []
            for i in objSelect:
                if search in i:
                    objMatch.append(i)
            if (len(objMatch) == 0):
                cmds.confirmDialog(t='Warning', m="Found nothing to be replaced!", b="Ok")
                sys.exit()
            else:
                i = 0
                for i in range(len(objMatch)):
                    str = objMatch[i]
                    newName = str.replace(search, replace)
                    cmds.rename(objMatch[i], newName)
                    self.doRenameShapes()
                    i += 1

    def addAttribute(self, *args):
        longName = cmds.textField('longNameAA', query=True, text=True)
        shortName = cmds.textField('shortNameAA', query=True, text=True)
        minNum = cmds.intField('minIntAA', query=True, v=True)
        defNum = cmds.intField('defIntAA', query=True, v=True)
        maxNum = cmds.intField('maxIntAA', query=True, v=True)
        ForB = cmds.optionMenu('ForBAA', query=True, v=True)
        objSelect = cmds.ls(sl=True)
        if (longName == ""):
            cmds.confirmDialog(t='Warning', m="Long Name field entry is blank!", b="Ok")
            cmds.warning("Long Name field entry is blank!")
            sys.exit()
        else:
            if (len(shortName) == 0):
                shortName = longName
            else:
                if (ForB == 'Boolean'):
                    for i in range(len(objSelect)):
                        cmds.select(objSelect[i])
                        cmds.addAttr(ln=longName, nn=shortName, at='bool', dv=1, k=True)
                        i += 1
                elif (ForB == 'Float'):
                    if (minNum == 0) and (maxNum == 0):
                        for i in range(len(objSelect)):
                            cmds.select(objSelect[i])
                            cmds.addAttr(ln=longName, nn=shortName, at='float', dv=defNum, k=True)
                            i += 1
                        cmds.warning("Min Value and Max Value are equal, ignore!")
                    elif (minNum > defNum) or (maxNum < defNum):
                        for i in range(len(objSelect)):
                            cmds.select(objSelect[i])
                            cmds.addAttr(ln=longName, nn=shortName, at='float', dv=defNum, k=True)
                            i += 1
                        cmds.warning("Min Value and Max Value are weird, ignore!")
                    else:
                        for i in range(len(objSelect)):
                            cmds.select(objSelect[i])
                            cmds.addAttr(ln=longName, nn=shortName, at='float', min=minNum, max=maxNum, dv=defNum,
                                         k=True)
                            i += 1

    def leftHandPreset(self, *args):
        objSelect = cmds.ls(sl=True)
        hand = ["thumb", "index", "middle", "ring", "little"]
        foot = ["big", "long", "middle", "ring", "pinky"]

        for i in range(len(objSelect)):
            cmds.select(objSelect[i])
            for item in range(len(hand)):
                longName = "L_" + hand[item] + "Finger_Curl"
                niceName = "L_" + hand[item] + "F_Curl"
                cmds.addAttr(ln=longName, nn=niceName, at='float', min=-5, dv=0, max=15, k=True)
                item += 1
            i += 1

    def rightHandPreset(self, *args):
        objSelect = cmds.ls(sl=True)
        hand = ["thumb", "index", "middle", "ring", "little"]
        foot = ["big", "long", "middle", "ring", "pinky"]
        for i in range(len(objSelect)):
            cmds.select(objSelect[i])
            for item in range(len(hand)):
                longName = "R_" + hand[item] + "Finger_Curl"
                niceName = "R_" + hand[item] + "F_Curl"
                cmds.addAttr(ln=longName, nn=niceName, at='float', min=-5, dv=0, max=15, k=True)
                item += 1
            i += 1

    def leftFootPreset(self, *args):
        objSelect = cmds.ls(sl=True)
        hand = ["thumb", "index", "middle", "ring", "little"]
        foot = ["big", "long", "middle", "ring", "pinky"]
        for i in range(len(objSelect)):
            cmds.select(objSelect[i])
            for item in range(len(foot)):
                longName = "L_" + foot[item] + "Toe_Curl"
                niceName = "L_" + foot[item] + "T_Curl"
                cmds.addAttr(ln=longName, nn=niceName, at='float', min=-5, dv=0, max=15, k=True)
                item += 1
            i += 1

    def rightFootPreset(self, *args):
        objSelect = cmds.ls(sl=True)
        hand = ["thumb", "index", "middle", "ring", "little"]
        foot = ["big", "long", "middle", "ring", "pinky"]
        for i in range(len(objSelect)):
            cmds.select(objSelect[i])
            for item in range(len(foot)):
                longName = "R_" + foot[item] + "Toe_Curl"
                niceName = "R_" + foot[item] + "T_Curl"
                cmds.addAttr(ln=longName, nn=niceName, at='float', min=-5, dv=0, max=15, k=True)
                item += 1
            i += 1

            # -------------------------------------------------------------------------------------------------------------
            # END OF CODE
            # -------------------------------------------------------------------------------------------------------------
