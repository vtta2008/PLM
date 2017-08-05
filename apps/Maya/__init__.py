import os
import sys
import maya.cmds as cmds

userAppScriptsDir = cmds.internalVar(usd=True)

scrDAMGtool = userAppScriptsDir + 'DAMGpipelineTool'

if os.path.exists(scrDAMGtool):
    if not scrDAMGtool in sys.path:
        sys.path.append(scrDAMGtool)
