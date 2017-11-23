# -*-coding:utf-8 -*
"""

Script Name: Tweener.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It will make a simple UI to tween the Animation line between 2 keyframes base on current frame.

"""
# -------------------------------------------------------------------------------------------------------------
# IMPORT MAYA PYTHON MODULES
# -------------------------------------------------------------------------------------------------------------
from maya import cmds
import sys

# ------------------------------------------------------
# VARIALBES ARE USED BY ALL CLASSES
# ------------------------------------------------------
winID = 'AnimationTweener'
winTitle = 'Tweener'
W = 430
CW = [(1,5),(2,100),(3,5),(4,25),(5,5),(6,200),(7,5),(8,80),(9,5)]

class Tweener(object):

    def __init__(self):

        super(Tweener, self).__init__()

        self.buildUI()


    def buildUI(self):

        if cmds.window(winID, query=True, exists=True):
            cmds.deleteUI(winID)

        cmds.window(winID, title=winTitle)

        column = cmds.columnLayout(w=W)

        cmds.text(l="")
        cmds.text(l="Use this slider to set the tween amount", align='center', w=W)
        cmds.text(l="")

        cmds.rowColumnLayout(nc=9, cw=CW)

        cmds.text(l='')
        self.floatField = cmds.floatField(min=0, max=100, v=50, pre=3, cc=self.changeSlider)
        cmds.text(l='')
        cmds.text(l='%')
        cmds.text(l='')
        self.slider = cmds.floatSlider(min=0, max=100, v=50, step=1, cc=self.tween)
        cmds.text(l='')
        cmds.button('Reset', c=self.reset)
        cmds.text(l='')

        cmds.showWindow(winID)

    def reset(self, *args):

        cmds.floatSlider(self.slider, edit=True, v=50)

        cmds.floatField(self.floatField, edit=True, v=50)

        self.tween(50)

    def changeSlider(self, *args):

        value = cmds.floatField(self.floatField, q=True, v=True)

        cmds.floatSlider(self.slider, edit=True, v=value)

        self.tween(value)

    def changeFloatField(self, *args):

        value = cmds.floatSlider(self.slider, q=True, v=True)

        cmds.floatField(self.floatField, e=True, v=value)

    def tween(self, percentage, obj=None, attrs=None, selection=True, *args):

        self.changeFloatField()

        # If obj is not given and selection is set to false error early
        if not obj and not selection:
            raise ValueError('No object given to tween')
        # If no obj is specified, get it from the first selection
        if not obj:
            curSel = cmds.ls(sl=True)

            if len(curSel)==0:
                print "There is nothing to tween"
                sys.exit()
            else:
                obj = cmds.ls(sl=True)[0]

        if not attrs:
            attrs = cmds.listAttr(obj, keyable=True)

        currentTime = cmds.currentTime(q=True)

        cmds.floatField(self.floatField, edit=True, v=percentage)

        for attr in attrs:
            # Construct the full name of the attribute with its object
            attrFull = '%s.%s' % (obj, attr)

            # Get the keyframes of the attribute on this project
            keyframes = cmds.keyframe(attrFull, query=True)

            # If there are no keyframes, then continue
            if not keyframes:
                continue

            previousKeyframes = [k for k in keyframes if k < currentTime]

            laterKeyframes = [k for k in keyframes if k > currentTime]

            if not previousKeyframes and not laterKeyframes:
                continue

            previousFrame = max(previousKeyframes) if previousKeyframes else None

            nextFrame = min(laterKeyframes) if laterKeyframes else None

            if not previousFrame or not nextFrame:
                continue

            previousValue = cmds.getAttr(attrFull, time=previousFrame)
            nextValue = cmds.getAttr(attrFull, time=nextFrame)

            difference = nextValue - previousValue
            weightedDifference = (difference * percentage) / 100.0
            currentValue = previousValue + weightedDifference

            cmds.setKeyframe(attrFull, time=currentTime, value=currentValue)

def initialize():
    Tweener()

if __name__ == "__main__":
    initialize()

# -------------------------------------------------------------------------------------------------------------
# END OF CODE
# -------------------------------------------------------------------------------------------------------------