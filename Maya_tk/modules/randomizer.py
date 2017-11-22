from maya import cmds
import random

def createObjects(mode, numObjects):
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
        
    return objList
   
def randomize(objList=None, minValue=0, maxValue=50):
    
    if objList is None:
        objList = cmds.ls(sl=True)
    
    for obj in objList:
        cmds.setAttr(obj+'.tx', random.randint(minValue, maxValue))
        cmds.setAttr(obj+'.ty', random.randint(minValue, maxValue))
        cmds.setAttr(obj+'.tz', random.randint(minValue, maxValue))