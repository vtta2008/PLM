# coding=utf-8

"""



"""

# -------------------------------------------------------------------------------------------------------------
""" About Plt """

__appname__ = "Pipeline Tool"
__module__ = "Plt"
__version__ = "13.0.1"
__organization__ = "DAMG team"
__website__ = "www.dot.damgteam.com"
__email__ = "dot@damgteam.com"
__author__ = "Trinh Do, a.k.a: Jimmy"
__root__ = "PLT_RT"
__db__ = "PLT_DB"
__st__ = "PLT_ST"

# -------------------------------------------------------------------------------------------------------------

import maya.cmds as cmds

class gear(object):
	def __init__(self):
		self.transform=None
		self.extrude=None
		self.extrude=None

	def createGear(self, teeth=10, length=0.3):
		spans = teeth*2
		self.transform, self.constructor = cmds.polyPipe(sa=spans)
		sideFaces = range(spans*2, spans*3, 2)
		cmds.select(clear=True)
		for face in sideFaces:
			cmds.select('%s.f[%s]' % (self.transform, face), add=True)
		self.extrude = cmds.polyExtrudeFacet(ltz=length)[0]

	def changeTeeth(self, constructor, extrude, teeth=10, length=0.3):
		spans = teeth*2
		cmds.polyPipe(self.constructor, edit=True, sa=spans)
		sideFaces = range(spans*2, spans*3, 2)
		faceNames = []
		for face in sideFaces:
			faceName = 'f[%s]' % (face)
			faceNames.append(faceName)
		cmds.setAttr('%s.inputComponents' % (extrude), len(faceNames), *faceNames, type="componentList")
		cmds.polyExtrudeFacet(self.extrude, edit=True, ltz=length)
