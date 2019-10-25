#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: WingCreator.py
Author: Do Trinh/Jimmy - TD artist

Description:
    It creates wing from locators importing from a file with rig

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import math
import maya.cmds as m

# Default variables (number of feathers, wing type)
numPrimaries = 10.0
numSecondaries = 13.0
numPrimaryCoverts = 10.0
numSecondaryCoverts = 13.0
numMedianCoverts = 13.0
numAlulas = 4
# numTertials = 3
wingType = 0

# temp variables for wingfold until I figure out a better way to do wingfolding
tempVarPrimary = 0
tempVarPrimaryCovert = 0
tempVarAlula = 0


# Function to run at startup- It creates the group structure for the rig
def runAtStartup():
    global my_wing
    global my_wing_type
    global wingType

    m.select(cl=True)

    # Create a layer for the feathers
    m.createDisplayLayer(noRecurse=True, name='FeathersLayer')

    # setup wings and wing type (hawk, falcon, etc.)
    my_wing = WingGroup("My Wing")
    my_wing_type = WingType("My Wings Type")

    # Create group hierarchy
    m.group(em=True, name='WingControls')
    m.group(em=True, name='Joints')
    m.group(em=True, name='NoXForm')
    m.group(em=True, name='FeatherGroups')
    m.group(em=True, name='Wings')
    m.group(em=True, name='XForm')

    # Create Main Control Base##################
    m.curve(n="MainWing_CON", d=1,
            p=[(0, 0.35, -1.001567), (-0.336638, 0.677886, -0.751175), (-0.0959835, 0.677886, -0.751175),
               (-0.0959835, 0.850458, -0.500783), (-0.0959835, 0.954001, -0.0987656), (-0.500783, 0.850458, -0.0987656),
               (-0.751175, 0.677886, -0.0987656), (-0.751175, 0.677886, -0.336638), (-1.001567, 0.35, 0),
               (-0.751175, 0.677886, 0.336638), (-0.751175, 0.677886, 0.0987656), (-0.500783, 0.850458, 0.0987656),
               (-0.0959835, 0.954001, 0.0987656), (-0.0959835, 0.850458, 0.500783), (-0.0959835, 0.677886, 0.751175),
               (-0.336638, 0.677886, 0.751175), (0, 0.35, 1.001567), (0.336638, 0.677886, 0.751175),
               (0.0959835, 0.677886, 0.751175), (0.0959835, 0.850458, 0.500783), (0.0959835, 0.954001, 0.0987656),
               (0.500783, 0.850458, 0.0987656), (0.751175, 0.677886, 0.0987656), (0.751175, 0.677886, 0.336638),
               (1.001567, 0.35, 0), (0.751175, 0.677886, -0.336638), (0.751175, 0.677886, -0.0987656),
               (0.500783, 0.850458, -0.0987656), (0.0959835, 0.954001, -0.0987656), (0.0959835, 0.850458, -0.500783),
               (0.0959835, 0.677886, -0.751175), (0.336638, 0.677886, -0.751175), (0, 0.35, -1.001567)])
    m.rotate('180deg', 0, 0, r=True)
    m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    m.hide('MainWing_CON')

    # Main control setup
    centerPosition = [0, 0, 0]
    shoulderPosition = m.xform(side + '_Wing_1', t=True, q=True, ws=True)  # Shoulder location coordinates
    # Find the distance from the origin to the shoulder so we know how much to scale the main control by
    distanceBetweenShoulder = distanceBetweenTwoPoints(centerPosition, shoulderPosition)
    m.select('MainWing_CON')
    m.scale(5 * distanceBetweenShoulder, 5 * distanceBetweenShoulder, 5 * distanceBetweenShoulder)
    m.move(0, shoulderPosition[1] - (2 * distanceBetweenShoulder), 0)
    m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    # Add color to the main wing Control
    m.select('MainWing_CON')  # Select the control
    # Pickwalk down to select the curve so that the parented objects are not also colored, only the control
    name = m.pickWalk(direction='down')
    m.setAttr(str(name[0]) + '.overrideEnabled', 1)
    m.setAttr(str(name[0]) + '.overrideColor', 17)  # Yellow

    m.parent
    m.parent
    m.parent
    m.parent
    m.parent
    m.parent

    m.select(cl=True)


## Classes definging wing group stuff and wing Type stuff
# Wing-group class, deals with the groups of the wing and methods to build those groups and controls
class WingGroup():
    def __init__(self, name):
        self.name = name

        # Method to buiild all the feathers in a group

    def buildFeathers(self, grpName, numFeathersInGroup, numBaseFeathers, LocatorA, LocatorB):
        # Calculate distance between both points
        DistX = (LocatorA[0] - LocatorB[0])
        DistY = (LocatorA[1] - LocatorB[1])
        DistZ = (LocatorA[2] - LocatorB[2])

        # Alulas build only 1/3 the distance along the wing bone, so divide the distance in third
        if (grpName == "_Alula_"):
            DistX = (1.0 / 3.0) * DistX
            DistY = (1.0 / 3.0) * DistY
            DistZ = (1.0 / 3.0) * DistZ

        # Divide by number of feathers to get the distance between each feather
        DistBetweenX = DistX / (numFeathersInGroup - 1)
        DistBetweenZ = DistZ / (numFeathersInGroup - 1)

        i = 1  # the step size for the function, so the function goes from 1-># of feathers
        if (grpName == "_Primaries_" or grpName == "_PrimaryCoverts_" or grpName == "_Alula_"):
            placementX = LocatorB[0]
            placementY = LocatorB[1]
            placementZ = LocatorB[2]
        elif (grpName == "_Secondaries_" or grpName == "_SecondaryCoverts_" or grpName == "_MedianCoverts_"):
            placementX = LocatorA[0]
            placementY = LocatorA[1]
            placementZ = LocatorA[2]

        newStep = (numBaseFeathers / numFeathersInGroup)  # New step size based on the original number of feathers,
        # Divide the base number of feathers by the new amount to
        # get the number to scale by for the function
        input = 1  # start function input at one then incriment it by the new step on each iteration

        # Duplicate feathers and move them into position
        while (i < (numFeathersInGroup + 1)):
            # duplicate from the base feather
            m.duplicate(side + grpName + 'Base', n=side + grpName + repr(i))
            m.select(side + grpName + repr(i))
            m.showHidden(side + grpName + repr(i))
            # Add it to the feathers layer
            m.editDisplayLayerMembers('FeathersLayer', side + grpName + repr(i))
            # move and rotate it into the correct place, account for stacking of different groups
            if (grpName == "_Primaries_" or grpName == "_Secondaries_"):
                m.move(placementX, placementY, placementZ, ws=True)
            elif (grpName == "_PrimaryCoverts_" or grpName == "_SecondaryCoverts_"):
                m.move(placementX, placementY + 0.2, placementZ, ws=True)
            elif (grpName == "_MedianCoverts_" or grpName == "_Alula_"):
                m.move(placementX, placementY + 0.4, placementZ, ws=True)

            # Rotate the feathers so they aren't flat, rotation direction changes based on if the character is facing
            # Down the Z axis, or up the z axis,
            if (side == "R"):
                if (grpName == "_Primaries_" or grpName == "_Secondaries_"):
                    m.rotate(0, 0, (facingDirection) * 5.0, r=True)
                elif (grpName == "_PrimaryCoverts_" or grpName == "_SecondaryCoverts_"):
                    m.rotate(0.5, 0, (facingDirection) * 5.0, r=True)
                elif (grpName == "_MedianCoverts_" or grpName == "_Alula_"):
                    m.rotate(0.8, 0, (facingDirection) * 5.0, r=True)
            elif (side == "L"):
                if (grpName == "_Primaries_" or grpName == "_Secondaries_"):
                    m.rotate(0, 0, (facingDirection) * -5.0, r=True)
                elif (grpName == "_PrimaryCoverts_" or grpName == "_SecondaryCoverts_"):
                    m.rotate(0.5, 0, (facingDirection) * -5.0, r=True)
                elif (grpName == "_MedianCoverts_" or grpName == "_Alula_"):
                    m.rotate(0.8, 0, (facingDirection) * -5.0, r=True)
            # Increase the placement for the next feather in the series by adding/subtracting the distance from the previous feather
            if (grpName == "_Primaries_" or grpName == "_PrimaryCoverts_" or grpName == "_Alula_"):
                placementX = placementX + DistBetweenX
                placementZ = placementZ + DistBetweenZ
            elif (grpName == "_Secondaries_" or grpName == "_SecondaryCoverts_" or grpName == "_MedianCoverts_"):
                placementX = placementX - DistBetweenX
                placementZ = placementZ - DistBetweenZ

            # Rotation and scale
            rotationVar = my_wing_type.makeType(grpName, input)[0]
            scaleVarZ = my_wing_type.makeType(grpName, input)[1]
            scaleVarX = my_wing_type.makeType(grpName, input)[2]

            m.select(side + grpName + repr(int(i)))  # Select the proper feather
            if (side == "R"):
                m.rotate(0, rotationVar, 0, r=True)  # Rotate it
            elif (side == "L"):
                m.rotate(0, -rotationVar, 0, r=True)
            m.scale(scaleVarX, 1, scaleVarZ, r=True)  # Scale it ############

            input = input + newStep;  # Incriment the step amount
            i = i + 1  # incriment the feather number

    # method to build and position the controls for the group
    def buildControls(self, grpName, scaleAmount1, scaleAmount2, jointA, jointB, startFeather, endFeather):

        # Create second control and move into position
        # Create two groups, one to use for the auto wingfold (_GRP2), one for correct positioning of the control (_GRP)
        m.group(em=True, name=side + grpName + 'Con_2_GRP2')
        m.delete(m.orientConstraint(side + grpName + repr(int(endFeather)),
                                    side + grpName + 'Con_2_GRP2'))  # Orient down the feather
        m.delete(m.pointConstraint(side + jointB, side + grpName + 'Con_2_GRP2'))  # Position at the Joint

        m.group(em=True, name=side + grpName + 'Con_2_GRP')
        m.delete(m.orientConstraint(side + grpName + repr(int(endFeather)),
                                    side + grpName + 'Con_2_GRP'))  # Orient down the feather
        m.delete(m.pointConstraint(side + jointB, side + grpName + 'Con_2_GRP'))  # Position at the Joint
        m.parent  # Parent the two groups properly

        m.group(em=True, name=side + grpName + 'Con_2_GRP_FLD')
        m.delete(m.orientConstraint(side + grpName + repr(int(endFeather)),
                                    side + grpName + 'Con_2_GRP_FLD'))  # Orient down the feather
        m.delete(m.pointConstraint(side + jointB, side + grpName + 'Con_2_GRP_FLD'))  # Position at the Joint
        m.parent  # Parent the two groups properly

        m.duplicate('ArrowConBase', n=side + grpName + 'Con_2')
        m.showHidden(side + grpName + 'Con_2')

        m.delete(m.orientConstraint(side + grpName + repr(int(endFeather)),
                                    side + grpName + 'Con_2'))  # Orient down the feather
        m.delete(m.pointConstraint(side + jointB, side + grpName + 'Con_2'))  # Position at the Joint

        m.select(side + grpName + 'Con_2')
        m.scale(scaleAmount2, scaleAmount2, scaleAmount2, r=True)  # Scale control based on the feathers locators

        m.parent
        m.select(side + grpName + 'Con_2')
        m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

        # Apply the correct color to the control
        colorControls(grpName + 'Con_2', 1)

        # Create first control and move into position
        # Create two groups, one to use for the auto wingfold (_GRP2), one for correct positioning of the control (_GRP)
        m.group(em=True, name=side + grpName + 'Con_1_GRP2')
        m.delete(m.orientConstraint(side + grpName + repr(int(endFeather)),
                                    side + grpName + 'Con_1_GRP2'))  # Orient down the feather
        m.delete(m.pointConstraint(side + jointB, side + grpName + 'Con_1_GRP2'))  # Position at the Joint

        m.group(em=True, name=side + grpName + 'Con_1_GRP')
        m.delete(m.orientConstraint(side + grpName + repr(int(startFeather)),
                                    side + grpName + 'Con_1_GRP'))  # Orient down the feather
        m.delete(m.pointConstraint(side + jointA, side + grpName + 'Con_1_GRP'))  # Position at the Joint
        m.parent  # Parent the two groups properly

        m.group(em=True, name=side + grpName + 'Con_1_GRP_FLD')
        m.delete(m.orientConstraint(side + grpName + repr(int(startFeather)),
                                    side + grpName + 'Con_1_GRP_FLD'))  # Orient down the feather
        m.delete(m.pointConstraint(side + jointA, side + grpName + 'Con_1_GRP_FLD'))  # Position at the Joint
        m.parent  # Parent the two groups properly

        m.duplicate('ArrowConBase', n=side + grpName + 'Con_1')
        m.showHidden(side + grpName + 'Con_1')
        m.delete(m.orientConstraint(side + grpName + repr(int(startFeather)),
                                    side + grpName + 'Con_1'))  # Orient down the feather
        m.delete(m.pointConstraint(side + jointA, side + grpName + 'Con_1'))  # Position at the Joint

        m.select(side + grpName + 'Con_1')
        m.scale(scaleAmount1, scaleAmount1, scaleAmount1, r=True)  # Scale control based on the feathers locators
        m.parent
        m.select(side + grpName + 'Con_1')
        m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

        colorControls(grpName + 'Con_1', 1)

    # Setup the Feather Groups   - Function takes in the feather name, number of feathers in the group, controls 1 and 2
    # and the wing joint that the group should be parented to
    def featherSetup(self, featherName, numFeathers, controlA, controlB, wingJoint):
        NAME = side + featherName
        i = 1

        # Create main group and move it to the rotation point
        m.group(em=True, name=NAME + 'GRP')
        m.move(m.getAttr(side + '_Wing_3.translateX'), m.getAttr(side + '_Wing_3.translateY'),
               m.getAttr(side + '_Wing_3.translateZ'), ws=True)

        # Create Groups for the feathers
        while (i < (numFeathers + 1)):
            FeatherName = NAME + repr(i)
            GRPName = NAME + repr(i) + "_GRP"
            m.group(em=True, name=GRPName)  # create a null group for each feather
            tester = m.xform(FeatherName + '.rotatePivot', t=True, q=True,
                             ws=True)  # Get the position of the feather's rotate point
            m.move(tester[0], Loc3Coord[1], tester[2],
                   ws=True)  # Move the group to the feathers rotate point so they're the same
            m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
            m.parent  # Parent feather to it's group
            m.parent  # Parent feather under proper main group
            i = i + 1
        m.select(cl=True)

        j = 1
        amount1 = 0.0
        amount2 = 1.0
        incriment = 1.0 / numFeathers  # Incriment by the percentage of the number of feathers

        # while loop takes each feather and orient constrains it to the two controls based on it's position in a wing
        # For example if feather 5 is in the center of the wing, it would be constrained 50% to control A and 50% to
        # control B.  Whereas Feather 2 may be closer to A, so it'd be 90% to A and 10% to B.
        # This is what caused the fanning motion of the feathers in a group between each control.
        while (j < (numFeathers + 1)):
            m.select(NAME + controlB, r=True)
            m.select(NAME + repr(j) + '_GRP', tgl=True)
            m.orientConstraint(weight=amount2, mo=True)
            amount2 = amount2 - incriment

            m.select(NAME + controlA, r=True)
            m.select(NAME + repr(j) + '_GRP', tgl=True)
            m.orientConstraint(weight=amount1, mo=True)
            amount1 = amount1 + incriment

            j = j + 1

            # Parent wing group to the joint for proper feather movement
        m.select(side + wingJoint, r=True)
        m.select(NAME + 'GRP', tgl=True)
        m.parentConstraint(weight=amount1, mo=True)
        m.select(cl=True)


# Takes the wing type specified by the user and the x value to calculate each feathers rotate and scale.
class WingType():
    def __init__(self, name):
        self.name = name

    # Calls the correct function based on the user input,
    # ses it the group name and the x location (input) to calculate
    # the rotation and scale for the feathers in each group for
    # the user specified wing type.
    def makeType(self, grpName, input):
        options = {0: self.hawk,
                   1: self.falcon
                   }

        return options[wingType](grpName, input)  # returns the Array of rotate and scale taken from the function

    # Function for a hawk wing
    def hawk(self, grpName, input):
        global tempVarPrimary, tempVarPrimaryCovert, tempVarAlula, tempVarPrimary2, tempVarPrimaryCovert2, tempVarAlula2

        # functions for each feather group in the wing type(Yes, there needs to be that many
        # significant digits, the function blows up without that much precision)
        if (grpName == "_Primaries_"):
            rotate = (0.0774 * math.pow(input, 2)) + (5.4107 * input) + 25.612
            scaleX = -(0.0018 * math.pow(input, 3)) + (0.029 * math.pow(input, 2)) - (0.1936 * input) + 1.3755
            scaleZ = -(0.0036 * math.pow(input, 3)) + (0.0457 * math.pow(input, 2)) - (0.1246 * input) + 0.9122
        elif (grpName == "_Secondaries_"):
            rotate = (0.112 * math.pow(input, 2)) - (5.5211 * input) + 28.011
            scaleX = (0.0002 * math.pow(input, 3)) - (0.0068 * math.pow(input, 2)) + (0.0366 * input) + 0.8348
            scaleZ = -(0.0042 * math.pow(input, 2)) + (0.0324 * input) + 0.9941
        elif (grpName == "_PrimaryCoverts_"):
            rotate = (0.0163 * math.pow(input, 2)) + (6.2671 * input) + 25.828
            scaleX = -(0.0008 * math.pow(input, 3)) + (0.0059 * math.pow(input, 2)) + (0.0035 * input) + 0.5301
            scaleZ = -(0.0028 * math.pow(input, 3)) + (0.0394 * math.pow(input, 2)) - (0.1444 * input) + 0.7414
        elif (grpName == "_SecondaryCoverts_"):
            rotate = (0.112 * math.pow(input, 2)) - (5.5211 * input) + 28.011
            scaleX = -(0.0025 * math.pow(input, 2)) + (0.0193 * input) + 0.5925
            scaleZ = -(0.0028 * math.pow(input, 2)) + (0.0216 * input) + 0.6627
        elif (grpName == "_MedianCoverts_"):
            rotate = -(0.0156 * math.pow(input, 3)) + (0.4273 * math.pow(input, 2)) - (7.182 * input) + 34.361
            scaleX = -(0.0059 * math.pow(input, 2)) + (0.0806 * input) + 0.4978
            scaleZ = -(0.0083 * math.pow(input, 2)) + (0.1161 * input) + 0.4887
        elif (grpName == "_Alula_"):
            rotate = -(0.5378 * math.pow(input, 2)) + (8.3916 * input) + 69.479
            scaleX = -(0.0265 * math.pow(input, 2)) + (0.1633 * input) + 0.4266
            scaleZ = -(0.0307 * math.pow(input, 2)) + (0.2373 * input) + 0.2896

        # Set temp variables for wingfolding
        tempVarPrimary2 = 12.172
        tempVarPrimaryCovert2 = 12.172
        tempVarAlula2 = 52.095
        tempVarPrimary = 0
        tempVarPrimaryCovert = 0
        tempVarAlula = 0

        return [rotate, scaleZ, scaleX]

    # Function for a falcon wing (currently a placeholder)
    def falcon(self, grpName, input):
        global tempVarPrimary, tempVarPrimaryCovert, tempVarAlula, tempVarPrimary2, tempVarPrimaryCovert2, tempVarAlula2

        if (grpName == "_Primaries_"):
            rotate = -(0.2466 * math.pow(input, 2)) + (6.7569 * input) + 28.742
            scaleZ = 0.847833 + (0.011857 * input) + (0.020540 * math.pow(input, 2)) - (0.001636 * math.pow(input, 3))
            scaleX = -(0.0003 * math.pow(input, 4)) + (0.0061 * math.pow(input, 3)) - (0.0425 * math.pow(input, 2)) + (
                0.1168 * input) + 0.8385
        elif (grpName == "_Secondaries_"):
            rotate = (0.03141 * math.pow(input, 2)) - (4.05779 * input) + 30.73998
            scaleZ = -(0.0009 * math.pow(input, 3)) + (0.0152 * math.pow(input, 2)) - (0.0758 * input) + 1.065
            scaleX = -(0.0005 * math.pow(input, 3)) + (0.0056 * math.pow(input, 2)) - (0.0142 * input) + 0.9397
        elif (grpName == "_PrimaryCoverts_"):
            rotate = -(0.0193 * math.pow(input, 2)) + (4.5758 * input) + 31.675
            scaleZ = 0.4440 + (0.131217 * input) - (0.033547 * math.pow(input, 2)) + (0.004439 * math.pow(input, 3)) - (
                0.000221 * math.pow(input, 4))
            scaleX = -(0.0028 * math.pow(input, 3)) + (0.0368 * math.pow(input, 2)) - (0.1128 * input) + 0.6304
        elif (grpName == "_SecondaryCoverts_"):
            rotate = -(0.01814 * math.pow(input, 2)) - (3.62964 * input) + 32.06956
            scaleZ = -(0.000653 * math.pow(input, 3)) + (0.010007 * math.pow(input, 2)) - (0.029386 * input) + 0.616636
            scaleX = -(0.0028 * math.pow(input, 2)) + (0.0216 * input) + 0.6627
        elif (grpName == "_MedianCoverts_"):
            rotate = (0.02479 * math.pow(input, 3)) - (0.63143 * math.pow(input, 2)) - (0.27553 * input) + 38.29868
            scaleZ = -(0.000116 * math.pow(input, 4)) + (0.003111 * math.pow(input, 3)) - (
                0.034471 * math.pow(input, 2)) + (0.194271 * input) + 0.341503
            scaleX = -(0.0083 * math.pow(input, 2)) + (0.1161 * input) + 0.4887
        elif (grpName == "_Alula_"):
            rotate = (0.0588 * math.pow(input, 2)) + (4.1137 * input) + 63.204
            scaleZ = (0.003 * math.pow(input, 2)) + (0.102 * input) + 0.6965
            scaleX = -(0.039 * math.pow(input, 2)) + (0.2138 * input) + 0.4823

        # Set temp variables for wingfolding
        tempVarPrimary = -20
        tempVarPrimary2 = 18
        tempVarPrimaryCovert = -15
        tempVarPrimaryCovert2 = 0
        tempVarAlula = -42
        tempVarAlula2 = 53

        return [rotate, scaleZ, scaleX]


## Rig Functions (Rig setup, Controls setup, blendshapes and such)
# Skeleton Setup
def generateSkeleton():
    m.select(cl=True)

    # If there's no skeleton on either side, then generate one
    if (m.objExists('R_Wing_1_JNT') == 0) and (m.objExists('L_Wing_1_JNT') == 0):
        # Create three skeletons- One for the IK, one for the FK and one for between
        # The between one is the one that is skinned to.
        # create the between skeleton for the wing
        m.joint(n=side + '_Wing_1_JNT',
                p=[m.getAttr(side + '_Wing_1.translateX'), m.getAttr(side + '_Wing_1.translateY'),
                   m.getAttr(side + '_Wing_1.translateZ')])
        m.joint(n=side + '_Wing_2_JNT',
                p=[m.getAttr(side + '_Wing_2.translateX'), m.getAttr(side + '_Wing_2.translateY'),
                   m.getAttr(side + '_Wing_2.translateZ')])
        m.joint(side + '_Wing_1_JNT', e=1, zso=1, oj='xyz')
        m.joint(n=side + '_Wing_3_JNT',
                p=[m.getAttr(side + '_Wing_3.translateX'), m.getAttr(side + '_Wing_3.translateY'),
                   m.getAttr(side + '_Wing_3.translateZ')])
        m.joint(side + '_Wing_2_JNT', e=1, zso=1, oj='xyz')
        m.joint(n=side + '_Wing_4_JNT',
                p=[m.getAttr(side + '_Wing_4.translateX'), m.getAttr(side + '_Wing_4.translateY'),
                   m.getAttr(side + '_Wing_4.translateZ')])
        m.joint(side + '_Wing_3_JNT', e=1, zso=1, oj='xyz')

        m.select(cl=True)
        # create the IK skeleton for the wing
        m.joint(n=side + '_Wing_1_JNT_IK',
                p=[m.getAttr(side + '_Wing_1.translateX'), m.getAttr(side + '_Wing_1.translateY'),
                   m.getAttr(side + '_Wing_1.translateZ')])
        m.joint(n=side + '_Wing_2_JNT_IK',
                p=[m.getAttr(side + '_Wing_2.translateX'), m.getAttr(side + '_Wing_2.translateY'),
                   m.getAttr(side + '_Wing_2.translateZ')])
        m.joint(side + '_Wing_1_JNT_IK', e=1, zso=1, oj='xyz', sao='yup')
        m.joint(n=side + '_Wing_3_JNT_IK',
                p=[m.getAttr(side + '_Wing_3.translateX'), m.getAttr(side + '_Wing_3.translateY'),
                   m.getAttr(side + '_Wing_3.translateZ')])
        m.joint(side + '_Wing_2_JNT_IK', e=1, zso=1, oj='xyz', sao='yup')
        m.joint(n=side + '_Wing_4_JNT_IK',
                p=[m.getAttr(side + '_Wing_4.translateX'), m.getAttr(side + '_Wing_4.translateY'),
                   m.getAttr(side + '_Wing_4.translateZ')])
        m.joint(side + '_Wing_3_JNT_IK', e=1, zso=1, oj='xyz', sao='yup')
        m.select(cl=True)

        # create the FK skeleton for the wing
        m.joint(n=side + '_Wing_1_JNT_FK',
                p=[m.getAttr(side + '_Wing_1.translateX'), m.getAttr(side + '_Wing_1.translateY'),
                   m.getAttr(side + '_Wing_1.translateZ')])
        m.joint(n=side + '_Wing_2_JNT_FK',
                p=[m.getAttr(side + '_Wing_2.translateX'), m.getAttr(side + '_Wing_2.translateY'),
                   m.getAttr(side + '_Wing_2.translateZ')])
        m.joint(side + '_Wing_1_JNT_FK', e=1, zso=1, oj='xyz', sao='yup')
        m.joint(n=side + '_Wing_3_JNT_FK',
                p=[m.getAttr(side + '_Wing_3.translateX'), m.getAttr(side + '_Wing_3.translateY'),
                   m.getAttr(side + '_Wing_3.translateZ')])
        m.joint(side + '_Wing_2_JNT_FK', e=1, zso=1, oj='xyz', sao='yup')
        m.joint(n=side + '_Wing_4_JNT_FK',
                p=[m.getAttr(side + '_Wing_4.translateX'), m.getAttr(side + '_Wing_4.translateY'),
                   m.getAttr(side + '_Wing_4.translateZ')])
        m.joint(side + '_Wing_3_JNT_FK', e=1, zso=1, oj='xyz', sao='yup')
        m.select(cl=True)
    else:  # If there is a skeleton on one side, Mirror the other side so that the behavior between the two is mirrored
        if (side == 'L'):
            m.mirrorJoint('R_Wing_1_JNT', mirrorYZ=True, mirrorBehavior=True, searchReplace=('R', 'L'))
            m.mirrorJoint('R_Wing_1_JNT_FK', mirrorYZ=True, mirrorBehavior=True, searchReplace=('R', 'L'))
            m.mirrorJoint('R_Wing_1_JNT_IK', mirrorYZ=True, mirrorBehavior=True, searchReplace=('R', 'L'))
        elif (side == 'R'):
            m.mirrorJoint('L_Wing_1_JNT', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L', 'R'))
            m.mirrorJoint('L_Wing_1_JNT_FK', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L', 'R'))
            m.mirrorJoint('L_Wing_1_JNT_IK', mirrorYZ=True, mirrorBehavior=True, searchReplace=('L', 'R'))

            # Move the mirrored joints into the correct position (wings are not always symmetrical, unfortunately)
            # counter = 1
            # while (counter < 5):
            #     value = repr(counter)
            #     m.move(m.getAttr(side + '_Wing_' + value + '.translateX'),
            #            m.getAttr(side + '_Wing_' + value + '.translateY'),
            #            m.getAttr(side + '_Wing_' + value + '.translateZ'), side + '_Wing_' + value + '_JNT',
            #            ws=True)  # move the pole vector control into place
            #     m.move(m.getAttr(side + '_Wing_' + value + '.translateX'),
            #            m.getAttr(side + '_Wing_' + value + '.translateY'),
            #            m.getAttr(side + '_Wing_' + value + '.translateZ'), side + '_Wing_' + value + '_JNT_IK',
            #            ws=True)  # move the pole vector control into place
            #     m.move(m.getAttr(side + '_Wing_' + value + '.translateX'),
            #            m.getAttr(side + '_Wing_' + value + '.translateY'),
            #            m.getAttr(side + '_Wing_' + value + '.translateZ'), side + '_Wing_' + value + '_JNT_FK',
            #            ws=True)  # move the pole vector control into place
            #     counter = counter + 1



            # Create control system


def controlsSetup():
    global tipLength, middleLength, insideLength

    # Use the bounding box of the feathers to figure out where the controls are supposed to be
    primariesBoundingBox = m.polyEvaluate(side + '_Primaries_' + repr(int(numPrimaries)), b=True)
    primaries2BoundingBox = m.polyEvaluate(side + '_Primaries_1', b=True)
    secondariesBoundingBox = m.polyEvaluate(side + '_Secondaries_1', b=True)
    secondaries2BoundingBox = m.polyEvaluate(side + '_Secondaries_' + repr(int(numSecondaries)), b=True)

    # Get the furthest corners of the bounding boxes surrounding the feathers where the controls generate (In this case,
    # furthest point in X for the tip control(controlsLocator1), furthest points in Z for the middle and end controls.
    # The middle control generates in between two feathers, so use the longest feathers bounding box.
    # The furthest control changes based on the direction the character is facing.
    if facingDirection == 1:
        if side == "R":
            controlsLocator1 = primariesBoundingBox[0][1]
        if side == "L":
            controlsLocator1 = primariesBoundingBox[0][0]
        if (abs(primaries2BoundingBox[2][1]) >= abs(secondariesBoundingBox[2][1])):
            controlsLocator2 = primaries2BoundingBox[2][1]
        else:
            controlsLocator2 = primaries2BoundingBox[2][1]
        controlsLocator3 = secondaries2BoundingBox[2][1]
    elif facingDirection == -1:
        if side == "R":
            controlsLocator1 = primariesBoundingBox[0][0]
        if side == "L":
            controlsLocator1 = primariesBoundingBox[0][1]
        if (abs(primaries2BoundingBox[2][0]) >= abs(secondariesBoundingBox[2][0])):
            controlsLocator2 = primaries2BoundingBox[2][0]
        else:
            controlsLocator2 = primaries2BoundingBox[2][0]
        controlsLocator3 = secondaries2BoundingBox[2][0]

    # Find the distance between the feathers furthes bounding box point and the control locator
    # These distances are used to set the controls so that they don't end up hidden in feathers
    tipLength = distanceBetweenTwoPoints(controlsLocator1, Loc3Coord[0])
    middleLength = distanceBetweenTwoPoints(controlsLocator2, Loc3Coord[2])
    insideLength = distanceBetweenTwoPoints(controlsLocator3, Loc2Coord[2])

    # Create Shoulder Control and move to shoulder position
    m.group(em=True, name=side + '_Shoulder_Con_GRP2')  # create the group
    m.delete(m.orientConstraint(side + '_Wing_1_JNT', side + '_Shoulder_Con_GRP2'))
    m.delete(m.pointConstraint(side + '_Wing_1_JNT', side + '_Shoulder_Con_GRP2'))  # position it

    m.group(em=True, name=side + '_Shoulder_Con_GRP')  # create the group
    m.delete(m.orientConstraint(side + '_Wing_1_JNT', side + '_Shoulder_Con_GRP'))
    m.delete(m.pointConstraint(side + '_Wing_1_JNT', side + '_Shoulder_Con_GRP'))  # position it
    m.parent  # Parent the groups properly

    m.duplicate('MoveAllConBase', n=side + '_Shoulder_CON')  # make the controller
    m.showHidden(side + '_Shoulder_CON')
    m.delete(m.orientConstraint(side + '_Wing_1_JNT', side + '_Shoulder_CON'))  # Position it to the joint
    m.delete(m.pointConstraint(side + '_Wing_1_JNT', side + '_Shoulder_CON'))  # Position it to the joint
    m.parent
    m.select(side + '_Shoulder_CON')
    m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)  # Cleanup channels

    # Create Wrist Control and move to wrist position
    m.group(em=True, name=side + '_Wrist_Con_GRP')  # Create the group
    # position and orient it to the joint properly
    m.delete(m.orientConstraint(side + '_Wing_3_JNT', side + '_Wrist_Con_GRP'))
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_Wrist_Con_GRP'))
    m.duplicate('BoxConBase', n=side + '_Wrist_CON')  # create the control
    m.showHidden(side + '_Wrist_CON')
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_Wrist_CON'))  # Position it to the joint
    m.parent
    m.select(side + '_Wrist_CON')
    m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)  # Cleanup channels

    ##Pole Vector Setup
    # Create Pole Vecor Control and move into position behind the wing
    m.polyCone(n=side + '_Wing_Pole_CON', r=1, h=2)
    m.move(m.getAttr(side + '_Wing_2.translateX'), m.getAttr(side + '_Wing_2.translateY'),
           (facingDirection) * (m.getAttr(side + '_Wing_2.translateZ') + middleLength + (0.4 * middleLength)),
           ws=True)  # move the pole vector control into place
    m.rotate('90deg', 0, 0, r=True)
    colorControls('_Wing_Pole_CON', 0)  # Color the control

    # Sub-Feather Controls
    # build Feather controls for each individual group
    # The fractions of the Lengths are to stagger the controls to make them visible and to make sure the controls are -longer- than where the Locators
    # define the edge of the wing.
    my_wing.buildControls("_Primaries_", (facingDirection) * (tipLength + (0.125 * tipLength)),
                          (facingDirection) * (middleLength + (0.15 * middleLength)), "_Wing_3_JNT", "_Wing_3_JNT",
                          numPrimaries, 1)
    my_wing.buildControls("_Secondaries_", (facingDirection) * (insideLength + (0.25 * insideLength)),
                          (facingDirection) * (middleLength + (0.15 * middleLength)), "_Wing_2_JNT", "_Wing_3_JNT",
                          numSecondaries, 1)
    my_wing.buildControls("_PrimaryCoverts_", (facingDirection) * (tipLength + (0.1 * tipLength)),
                          (facingDirection) * (middleLength + (0.1 * middleLength)), "_Wing_3_JNT", "_Wing_3_JNT",
                          numPrimaryCoverts, 1)
    my_wing.buildControls("_SecondaryCoverts_", (facingDirection) * (insideLength + (0.2 * insideLength)),
                          (facingDirection) * (middleLength + (0.1 * middleLength)), "_Wing_2_JNT", "_Wing_3_JNT",
                          numSecondaryCoverts, 1)
    my_wing.buildControls("_MedianCoverts_", (facingDirection) * (insideLength + (0.15 * insideLength)),
                          (facingDirection) * (middleLength + (0.05 * middleLength)), "_Wing_2_JNT", "_Wing_3_JNT",
                          numMedianCoverts, 1)
    my_wing.buildControls("_Alula_", (facingDirection) * (tipLength + (0.05 * tipLength)),
                          (facingDirection) * (tipLength + (0.075 * tipLength)), "_Wing_3_JNT", "_Wing_3_JNT",
                          numAlulas, 1)

    # Build IK FK Switch
    IKFKControlSetup()

    # Parent Wrist rotation to the Wrist con
    m.select(side + '_Wrist_CON', r=True)
    m.select(side + '_Wing_3_JNT_IK', tgl=True)
    m.orientConstraint(weight=1, mo=True)

    # Correctly Parent control system
    m.parent
    m.parent

    # Constrain the pole vector
    m.poleVectorConstraint(side + '_Wing_Pole_CON', side + '_Wing_IK')
    m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    # Parent Joints to the Shoulder control
    m.select(side + '_Shoulder_CON', r=True)
    m.select(side + '_Wing_1_JNT', tgl=True)
    m.pointConstraint(weight=1, mo=True)

    m.select(side + '_Shoulder_CON', r=True)
    m.select(side + '_Wing_1_JNT_FK', tgl=True)
    m.parentConstraint(weight=1, mo=True)

    m.select(side + '_Shoulder_CON', r=True)
    m.select(side + '_Wing_1_JNT_IK', tgl=True)
    m.pointConstraint(weight=1, mo=True)

    # Parent FK controls to shoulder control
    m.parent
    m.parent

    # Add colors to controls
    colorControls('_Wrist_CON', 0)
    colorControls('_Shoulder_CON', 0)

    m.select(cl=True)


# Create the base controls used in the program
# Note: To change a control shape in the entire program, change the base control in this function
# this will apply it to all instances of that control in the final rig.
# Create Wing Controls
def createWingControls():
    # Create MoveAll Control Base
    m.curve(n="MoveAllConBase", d=1,
            p=[(0, 0, -9.41), (0, 2.82, -5.18), (0, 1.41, -5.18), (0, 1.41, -1.41), (0, 5.18, -1.41), (0, 5.18, -2.81),
               (0, 9.41, 0), (0, 5.18, 2.82), (0, 5.18, 1.41), (0, 1.41, 1.41), (0, 1.41, 5.18), (0, 2.82, 5.18),
               (0, 0, 9.41), (0, -2.82, 5.18), (0, -1.41, 5.18), (0, -1.41, 1.41), (0, -5.18, 1.41), (0, -5.18, 2.82),
               (0, -9.41, 0), (0, -5.18, -2.81), (0, -5.18, -1.41), (0, -1.41, -1.41), (0, -1.41, -5.18),
               (0, -2.82, -5.18), (0, 0, -9.41)])

    # Create Con Base
    m.curve(n="CONBASE", d=1, p=[(0, 0, 0), (0, 0, 25.4), (-1, 0, 24.4), (0, 0, 25.4), (1, 0, 24.4)])

    # Create Box Control Base
    m.curve(n="BoxConBase", d=1,
            p=[(-2, -2, 2), (-2, -2, -2), (2, -2, -2), (2, 2, -2), (-2, 2, -2), (-2, -2, -2), (2, -2, -2), (2, -2, 2),
               (-2, -2, 2), (-2, 2, 2), (-2, 2, -2), (2, 2, -2), (2, 2, 2), (-2, 2, 2), (2, 2, 2), (2, -2, 2)])

    # Create Arrow Controls Base
    m.curve(n="ArrowConBase", d=1, p=[(0, 0, 0), (0, 0, 1), (-0.0393, 0, .96), (0, 0, 1), (0.0393, 0, .96)])

    # Create Curve Control Base
    m.curve(n="CurveConBase", d=1,
            p=[(-0.174, 0, 0.985), (-0.0872, 0, 0.997), (0, 0, 1), (0.0872, 0, 0.997), (0.174, 0, 0.985)])

    # Create wing Flex controls for the Curve Control Base
    if (m.objExists(side + '_Primaries_BLND')) or (m.objExists(side + '_Secondaries_BLND')):
        m.circle(n="Wing_Flex_1", c=(0.1, 0, 1.1), nr=(0, 1, 0), r=0.05)
        m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        m.xform(cp=1)
        m.circle(n="Wing_Flex_1", c=(-0.1, 0, 1.1), nr=(0, 1, 0), r=0.05)
        m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
        m.xform(cp=1)
        # parent the wing flex conrtols to the curve control
        m.parent
        m.parent


def removeConstraints(target):
    constraints = m.listRelatives(target, type="constraint")
    global side
    if constraints:
        for constraint in constraints:
            if (side + "_") not in constraint:
                print "Incorrect Constraint Found: " + constraint
                print "Target: " + target
                m.delete(constraint)
        print "Found Contraints on: " + target


# Creates the IK and FK controls
def IKFKControlSetup():
    # Create IK control
    m.select(d=True)
    m.ikHandle(sj=side + '_Wing_1_JNT_IK', ee=side + '_Wing_3_JNT_IK', p=2, w=.5, sol='ikRPsolver')  # Step 11
    m.rename(side + '_Wing_IK')

    removeConstraints(side + '_Wing_IK')
    # Parent wrist Con to the IK
    m.select(side + '_Wrist_CON', r=True)
    m.select(side + '_Wing_IK', tgl=True)
    m.pointConstraint(weight=1, mo=True)

    # Orient constrain joint hierarchy for transition skeleton to IK and FK skeletons
    removeConstraints(side + '_Wing_1_JNT')
    m.select(side + '_Wing_1_JNT_IK', r=True)
    m.select(side + '_Wing_1_JNT_FK', tgl=True)
    m.select(side + '_Wing_1_JNT', tgl=True)
    m.orientConstraint(weight=1, mo=True)

    removeConstraints(side + '_Wing_2_JNT')
    m.select(side + '_Wing_2_JNT_IK', r=True)
    m.select(side + '_Wing_2_JNT_FK', tgl=True)
    m.select(side + '_Wing_2_JNT', tgl=True)
    m.orientConstraint(weight=1, mo=True)

    removeConstraints(side + '_Wing_1_JNT')
    m.select(side + '_Wing_3_JNT_IK', r=True)
    m.select(side + '_Wing_3_JNT_FK', tgl=True)
    m.select(side + '_Wing_3_JNT', tgl=True)
    m.orientConstraint(weight=1, mo=True)

    # CHANGE INTERPOLATION TYPES ON ORIENT CONSTRAINTS
    m.setAttr(side + '_Wing_1_JNT_orientConstraint1.interpType', 2);
    m.setAttr(side + '_Wing_2_JNT_orientConstraint1.interpType', 2);
    m.setAttr(side + '_Wing_3_JNT_orientConstraint1.interpType', 2);

    # Create Switch attribute
    m.addItem(side + '_Shoulder_CON', longName='IK_FK_Switch', defaultValue=0.0, minValue=0.0, maxValue=10.0)
    m.setAttr(side + '_Shoulder_CON.' + 'IK_FK_Switch', k=1)  # Make it keyable

    # Set switch to alternate between IK and FK orient constraints using set driven envKeys
    m.setAttr(side + '_Wing_1_JNT_orientConstraint1.' + side + '_Wing_1_JNT_IKW0', 1)
    m.setAttr(side + '_Wing_1_JNT_orientConstraint1.' + side + '_Wing_1_JNT_FKW1', 0)

    m.setDrivenKeyframe(side + '_Wing_1_JNT_orientConstraint1.' + side + '_Wing_1_JNT_IKW0',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_1_JNT_orientConstraint1.' + side + '_Wing_1_JNT_FKW1',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')

    m.setAttr(side + '_Wing_2_JNT_orientConstraint1.' + side + '_Wing_2_JNT_IKW0', 1)
    m.setAttr(side + '_Wing_2_JNT_orientConstraint1.' + side + '_Wing_2_JNT_FKW1', 0)

    m.setDrivenKeyframe(side + '_Wing_2_JNT_orientConstraint1.' + side + '_Wing_2_JNT_IKW0',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_2_JNT_orientConstraint1.' + side + '_Wing_2_JNT_FKW1',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')

    m.setAttr(side + '_Wing_3_JNT_orientConstraint1.' + side + '_Wing_3_JNT_IKW0', 1)
    m.setAttr(side + '_Wing_3_JNT_orientConstraint1.' + side + '_Wing_3_JNT_FKW1', 0)

    m.setDrivenKeyframe(side + '_Wing_3_JNT_orientConstraint1.' + side + '_Wing_3_JNT_IKW0',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_3_JNT_orientConstraint1.' + side + '_Wing_3_JNT_FKW1',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')

    m.setAttr(side + '_Shoulder_CON.IK_FK_Switch', 10)
    m.setAttr(side + '_Wing_1_JNT_orientConstraint1.' + side + '_Wing_1_JNT_IKW0', 0)
    m.setAttr(side + '_Wing_1_JNT_orientConstraint1.' + side + '_Wing_1_JNT_FKW1', 1)

    m.setDrivenKeyframe(side + '_Wing_1_JNT_orientConstraint1.' + side + '_Wing_1_JNT_IKW0',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_1_JNT_orientConstraint1.' + side + '_Wing_1_JNT_FKW1',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')

    m.setAttr(side + '_Wing_2_JNT_orientConstraint1.' + side + '_Wing_2_JNT_IKW0', 0)
    m.setAttr(side + '_Wing_2_JNT_orientConstraint1.' + side + '_Wing_2_JNT_FKW1', 1)

    m.setDrivenKeyframe(side + '_Wing_2_JNT_orientConstraint1.' + side + '_Wing_2_JNT_IKW0',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_2_JNT_orientConstraint1.' + side + '_Wing_2_JNT_FKW1',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')

    m.setAttr(side + '_Wing_3_JNT_orientConstraint1.' + side + '_Wing_3_JNT_IKW0', 0)
    m.setAttr(side + '_Wing_3_JNT_orientConstraint1.' + side + '_Wing_3_JNT_FKW1', 1)

    m.setDrivenKeyframe(side + '_Wing_3_JNT_orientConstraint1.' + side + '_Wing_3_JNT_IKW0',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_3_JNT_orientConstraint1.' + side + '_Wing_3_JNT_FKW1',
                        cd=side + '_Shoulder_CON.IK_FK_Switch')

    # Create FK Controllers
    # Controller 2
    m.group(em=True, name=side + '_Wing2_FK_Con_GRP2')
    m.delete(m.orientConstraint(side + '_Wing_2_JNT', side + '_Wing2_FK_Con_GRP2'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_2_JNT', side + '_Wing2_FK_Con_GRP2'))  # Position at the Joint

    m.group(em=True, name=side + '_Wing2_FK_Con_GRP')
    m.delete(m.orientConstraint(side + '_Wing_2_JNT', side + '_Wing2_FK_Con_GRP'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_2_JNT', side + '_Wing2_FK_Con_GRP'))  # Position at the Joint
    m.parent  # Parent them properly

    m.circle(nr=(4, 0, 0), c=(0, 0, 0), r=5, n=side + '_Wing2_FK_CON')
    m.delete(m.orientConstraint(side + '_Wing_2_JNT', side + '_Wing2_FK_CON'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_2_JNT', side + '_Wing2_FK_CON'))  # Position at the Joint

    m.parent
    m.select(side + '_Wing2_FK_CON')
    m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    colorControls('_Wing2_FK_CON', 0)

    # Controller 3
    m.group(em=True, name=side + '_Wing3_FK_Con_GRP2')
    m.delete(m.orientConstraint(side + '_Wing_3_JNT', side + '_Wing3_FK_Con_GRP2'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_Wing3_FK_Con_GRP2'))  # Position at the Joint

    m.group(em=True, name=side + '_Wing3_FK_Con_GRP')
    m.delete(m.orientConstraint(side + '_Wing_3_JNT', side + '_Wing3_FK_Con_GRP'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_Wing3_FK_Con_GRP'))  # Position at the Joint
    m.parent  # Parent them properly

    m.circle(nr=(4, 0, 0), c=(0, 0, 0), r=5, n=side + '_Wing3_FK_CON')
    m.delete(m.orientConstraint(side + '_Wing_3_JNT', side + '_Wing3_FK_CON'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_Wing3_FK_CON'))  # Position at the Joint

    m.parent
    m.select(side + '_Wing3_FK_CON')
    m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    colorControls('_Wing3_FK_CON', 0)

    # Parent the controls to the joint
    removeConstraints(side + '_Wing_2_JNT_FK')
    m.select(side + '_Wing2_FK_CON', r=True)
    m.select(side + '_Wing_2_JNT_FK', tgl=True)
    m.orientConstraint(weight=1, mo=True)

    # Parent the controls to the joint
    removeConstraints(side + '_Wing_3_JNT_FK')
    m.select(side + '_Wing3_FK_CON', r=True)
    m.select(side + '_Wing_3_JNT_FK', tgl=True)
    m.orientConstraint(weight=1, mo=True)

    # set visibility of IK/FK switch
    m.setAttr(side + '_Shoulder_CON.IK_FK_Switch', 0)

    # Visibility for IK fn
    m.setAttr(side + '_Wing2_FK_Con_GRP.visibility', 0)
    m.setAttr(side + '_Wing3_FK_Con_GRP.visibility', 0)
    m.setAttr(side + '_Wing_1_JNT_FK.visibility', 0)
    m.setAttr(side + '_Wrist_Con_GRP.visibility', 1)
    m.setAttr(side + '_Wing_1_JNT_IK.visibility', 1)
    m.setAttr(side + '_Wing_Pole_CON.visibility', 1)

    m.setDrivenKeyframe(side + '_Wing2_FK_Con_GRP.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing3_FK_Con_GRP.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wrist_Con_GRP.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_1_JNT_IK.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_1_JNT_FK.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_Pole_CON.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')

    # Visibility for FK fn
    m.setAttr(side + '_Shoulder_CON.IK_FK_Switch', 1)
    m.setAttr(side + '_Wing2_FK_Con_GRP.visibility', 1)
    m.setAttr(side + '_Wing3_FK_Con_GRP.visibility', 1)
    m.setAttr(side + '_Wing_1_JNT_FK.visibility', 1)
    m.setAttr(side + '_Wrist_Con_GRP.visibility', 0)
    m.setAttr(side + '_Wing_1_JNT_IK.visibility', 0)
    m.setAttr(side + '_Wing_Pole_CON.visibility', 0)

    m.setDrivenKeyframe(side + '_Wing2_FK_Con_GRP.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing3_FK_Con_GRP.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wrist_Con_GRP.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_1_JNT_IK.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_1_JNT_FK.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')
    m.setDrivenKeyframe(side + '_Wing_Pole_CON.visibility', cd=side + '_Shoulder_CON.IK_FK_Switch')

    # Set control back to Default 0 (sets it to default IK fn)
    m.setAttr(side + '_Shoulder_CON.IK_FK_Switch', 0)
    m.select(cl=True)


# Main controls setup
def mainControls():
    # Create Feathers Tips Control #
    # Create two groups, one to use for the auto wingfold (_GRP2), one for correct positioning of the control (_GRP)
    m.group(em=True, name=side + '_TipFeathers_GRP2')
    m.delete(m.orientConstraint(side + '_Primaries_' + repr(int(numPrimaries)),
                                side + '_TipFeathers_GRP2'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_TipFeathers_GRP2'))  # Position it

    m.group(em=True, name=side + '_TipFeathers_GRP')
    m.delete(m.orientConstraint(side + '_Primaries_' + repr(int(numPrimaries)),
                                side + '_TipFeathers_GRP'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_TipFeathers_GRP'))  # Position it
    m.parent  # Parent them properly

    m.group(em=True, name=side + '_TipFeathers_GRP_FLD')
    m.delete(m.orientConstraint(side + '_Primaries_' + repr(int(numPrimaries)),
                                side + '_TipFeathers_GRP_FLD'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_TipFeathers_GRP_FLD'))  # Position it
    m.parent  # Parent them properly

    # Make the control
    m.duplicate('CurveConBase', n=side + '_TipFeathers_CON')
    m.showHidden(side + '_TipFeathers_CON')
    # Position it properly
    m.select(side + '_TipFeathers_CON')
    m.delete(m.orientConstraint(side + '_Primaries_' + repr(int(numPrimaries)),
                                side + '_TipFeathers_CON'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_TipFeathers_CON'))  # Position it

    # Scale the length of the control based on the position of the locators plus a percentage of the longest control so that they're past
    # the feather tips and don't get lost in them
    scaleLengthTip = (facingDirection) * (tipLength + (0.15 * tipLength))
    m.scale(scaleLengthTip, scaleLengthTip, scaleLengthTip, r=True)
    m.parent
    m.select(side + '_TipFeathers_CON')
    m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    # color the control
    colorControls('_TipFeathers_CON', 0)

    # Create Feathers Middle Control #
    # Calculate where the control should sit based on where the primary and secondary controls are.
    PrimaryPos = [m.getAttr(side + '_Primaries_1.rotateX'), m.getAttr(side + '_Primaries_1.rotateY'),
                  m.getAttr(side + '_Primaries_1.rotateZ')]
    SecondaryPos = [m.getAttr(side + '_Secondaries_1.rotateX'), m.getAttr(side + '_Secondaries_1.rotateY'),
                    m.getAttr(side + '_Secondaries_1.rotateZ')]
    HalfwayPos = [(PrimaryPos[0] - SecondaryPos[0]) / 2.0, (PrimaryPos[1] - SecondaryPos[1]) / 2.0,
                  (PrimaryPos[2] - SecondaryPos[2]) / 2.0]

    # Create two groups, one to use for the auto wingfold (_GRP2), one for correct positioning of the control (_GRP)
    m.group(em=True, name=side + '_MiddleFeathers_GRP2')
    m.rotate(SecondaryPos[0] + HalfwayPos[0], SecondaryPos[1] + HalfwayPos[1],
             SecondaryPos[2] + HalfwayPos[2])  # Rotate it in between the two controls
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_MiddleFeathers_GRP2'))  # Position it

    m.group(em=True, name=side + '_MiddleFeathers_GRP')
    m.rotate(SecondaryPos[0] + HalfwayPos[0], SecondaryPos[1] + HalfwayPos[1],
             SecondaryPos[2] + HalfwayPos[2])  # Rotate it in between the two controls
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_MiddleFeathers_GRP'))  # Position it
    m.parent  # Parent them properly

    m.group(em=True, name=side + '_MiddleFeathers_GRP_FLD')
    m.rotate(SecondaryPos[0] + HalfwayPos[0], SecondaryPos[1] + HalfwayPos[1],
             SecondaryPos[2] + HalfwayPos[2])  # Rotate it in between the two controls
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_MiddleFeathers_GRP_FLD'))  # Position it
    m.parent  # Parent them properly

    # Make the control
    m.duplicate('CurveConBase', n=side + '_MiddleFeathers_CON')
    m.showHidden(side + '_MiddleFeathers_CON')
    # Position it properly
    m.select(side + '_MiddleFeathers_CON')
    m.rotate(SecondaryPos[0] + HalfwayPos[0], SecondaryPos[1] + HalfwayPos[1],
             SecondaryPos[2] + HalfwayPos[2])  # Rotate it in between the two controls
    m.delete(m.pointConstraint(side + '_Wing_3_JNT', side + '_MiddleFeathers_CON'))  # Position it

    # Scale the length of the control based on the position of the locators plus a percentage of the longest control so that they're past
    # the feather tips and don't get lost in them
    scaleLengthMiddle = (facingDirection) * (middleLength + (0.2 * middleLength))
    m.scale(scaleLengthMiddle, scaleLengthMiddle, scaleLengthMiddle, r=True)
    m.parent
    m.select(side + '_MiddleFeathers_CON')
    m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    # color the control
    colorControls('_MiddleFeathers_CON', 0)

    # Feathers End Control #
    m.group(em=True, name=side + '_EndFeathers_GRP2')
    m.delete(m.orientConstraint(side + '_Secondaries_' + repr(int(numSecondaries)),
                                side + '_EndFeathers_GRP2'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_2_JNT', side + '_EndFeathers_GRP2'))  # Position it

    m.group(em=True, name=side + '_EndFeathers_GRP')
    m.delete(m.orientConstraint(side + '_Secondaries_' + repr(int(numSecondaries)),
                                side + '_EndFeathers_GRP'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_2_JNT', side + '_EndFeathers_GRP'))  # Position it
    m.parent  # Parent them properly

    m.group(em=True, name=side + '_EndFeathers_GRP_FLD')
    m.delete(m.orientConstraint(side + '_Secondaries_' + repr(int(numSecondaries)),
                                side + '_EndFeathers_GRP_FLD'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_2_JNT', side + '_EndFeathers_GRP_FLD'))  # Position it
    m.parent  # Parent them properly

    # Make the control
    m.duplicate('CurveConBase', n=side + '_EndFeathers_CON')
    m.showHidden(side + '_EndFeathers_CON')
    # Position it properly
    m.select(side + '_EndFeathers_CON')
    m.delete(m.orientConstraint(side + '_Secondaries_' + repr(int(numSecondaries)),
                                side + '_EndFeathers_CON'))  # Orient down the feather
    m.delete(m.pointConstraint(side + '_Wing_2_JNT', side + '_EndFeathers_CON'))  # Position it

    # Scale the length of the control based on the position of the locators plus a percentage of the longest control so that they're past
    # the feather tips and don't get lost in them
    scaleLengthEnd = (facingDirection) * (insideLength + (0.3 * insideLength))
    m.scale(scaleLengthEnd, scaleLengthEnd, scaleLengthEnd, r=True)
    m.parent
    m.select(side + '_EndFeathers_CON')
    m.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    # color the control
    colorControls('_EndFeathers_CON', 0)

    # Delete Extraneous Flex Controls
    if (m.objExists(side + '_Primaries_BLND')) or (m.objExists(side + '_Secondaries_BLND')):
        if (side == "L"):
            m.delete(side + '_TipFeathers_CON|Wing_Flex_2',
                     side + '_EndFeathers_CON|Wing_Flex_1')  # Remove the extra control
        elif (side == "R"):
            m.delete(side + '_TipFeathers_CON|Wing_Flex_1',
                     side + '_EndFeathers_CON|Wing_Flex_2')  # Remove the extra control

        # Name the flex controls properly
        if (side == "L"):
            m.rename(side + '_TipFeathers_CON|Wing_Flex_1', side + '_Tip_Flex_Feathers')
            m.rename(side + '_MiddleFeathers_CON|Wing_Flex_1', side + '_Mid_R_Flex_Feathers')
            m.rename(side + '_MiddleFeathers_CON|Wing_Flex_2', side + '_Mid_L_Flex_Feathers')
            m.rename(side + '_EndFeathers_CON|Wing_Flex_2', side + '_End_Flex_Feathers')
        elif (side == "R"):
            m.rename(side + '_TipFeathers_CON|Wing_Flex_2', side + '_Tip_Flex_Feathers')
            m.rename(side + '_MiddleFeathers_CON|Wing_Flex_2', side + '_Mid_R_Flex_Feathers')
            m.rename(side + '_MiddleFeathers_CON|Wing_Flex_1', side + '_Mid_L_Flex_Feathers')
            m.rename(side + '_EndFeathers_CON|Wing_Flex_1', side + '_End_Flex_Feathers')

        # Color the Controls Properly
        colorControls('_Tip_Flex_Feathers', 1)
        colorControls('_Mid_R_Flex_Feathers', 1)
        colorControls('_Mid_L_Flex_Feathers', 1)
        colorControls('_End_Flex_Feathers', 1)

    # Parent controls under the joints for proper movement (even between IK and FK)
    m.select(side + '_Wing_3_JNT', r=True)
    m.select(side + '_TipFeathers_GRP2', tgl=True)
    m.parentConstraint(weight=1, mo=True)

    m.select(side + '_Wing_3_JNT', r=True)
    m.select(side + '_MiddleFeathers_GRP2', tgl=True)
    m.parentConstraint(weight=1, mo=True)

    m.select(side + '_Wing_2_JNT', r=True)
    m.select(side + '_EndFeathers_GRP2', tgl=True)
    m.parentConstraint(weight=1, mo=True)

    # Parent The minor controls
    m.parent
    m.parent

    m.parent
    m.parent

    m.parent
    m.parent

    m.parent
    m.parent

    m.parent
    m.parent

    m.parent
    m.parent

    # Setup visibility Controls on the Overall Controls
    # Tip Feathers Controls #
    # Create Control Attributes
    m.addItem(side + '_TipFeathers_CON', longName='GroupControls', defaultValue=0.0, minValue=0.0, maxValue=1.0)
    m.setAttr(side + '_TipFeathers_CON.GroupControls', k=1)  # Make it keyable

    # Key them for on and off
    m.setAttr(side + '_TipFeathers_CON.GroupControls', 0)
    m.setAttr(side + '_Alula_Con_1.visibility', 0)
    m.setAttr(side + '_Primaries_Con_1.visibility', 0)
    m.setAttr(side + '_PrimaryCoverts_Con_1.visibility', 0)

    m.setDrivenKeyframe(side + '_Alula_Con_1.visibility', cd=side + '_TipFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_Primaries_Con_1.visibility', cd=side + '_TipFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_PrimaryCoverts_Con_1.visibility', cd=side + '_TipFeathers_CON.GroupControls')

    m.setAttr(side + '_TipFeathers_CON.GroupControls', 1)
    m.setAttr(side + '_Alula_Con_1.visibility', 1)
    m.setAttr(side + '_Primaries_Con_1.visibility', 1)
    m.setAttr(side + '_PrimaryCoverts_Con_1.visibility', 1)

    m.setDrivenKeyframe(side + '_Alula_Con_1.visibility', cd=side + '_TipFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_Primaries_Con_1.visibility', cd=side + '_TipFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_PrimaryCoverts_Con_1.visibility', cd=side + '_TipFeathers_CON.GroupControls')

    # Middle Feathers Controls #
    # Create Control Attributes
    m.addItem(side + '_MiddleFeathers_CON', longName='GroupControls', defaultValue=0.0, minValue=0.0, maxValue=1.0)
    m.setAttr(side + '_MiddleFeathers_CON.GroupControls', k=1)  # Make it keyable

    # Key them for on and off
    m.setAttr(side + '_MiddleFeathers_CON.GroupControls', 0)
    m.setAttr(side + '_Alula_Con_2.visibility', 0)
    m.setAttr(side + '_Primaries_Con_2.visibility', 0)
    m.setAttr(side + '_PrimaryCoverts_Con_2.visibility', 0)
    m.setAttr(side + '_MedianCoverts_Con_2.visibility', 0)
    m.setAttr(side + '_Secondaries_Con_2.visibility', 0)
    m.setAttr(side + '_SecondaryCoverts_Con_2.visibility', 0)

    m.setDrivenKeyframe(side + '_Alula_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_Primaries_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_PrimaryCoverts_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_MedianCoverts_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_Secondaries_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_SecondaryCoverts_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')

    m.setAttr(side + '_MiddleFeathers_CON.GroupControls', 1)
    m.setAttr(side + '_Alula_Con_2.visibility', 1)
    m.setAttr(side + '_Primaries_Con_2.visibility', 1)
    m.setAttr(side + '_PrimaryCoverts_Con_2.visibility', 1)
    m.setAttr(side + '_MedianCoverts_Con_2.visibility', 1)
    m.setAttr(side + '_Secondaries_Con_2.visibility', 1)
    m.setAttr(side + '_SecondaryCoverts_Con_2.visibility', 1)

    m.setDrivenKeyframe(side + '_Alula_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_Primaries_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_PrimaryCoverts_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_MedianCoverts_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_Secondaries_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_SecondaryCoverts_Con_2.visibility', cd=side + '_MiddleFeathers_CON.GroupControls')

    # End Feathers Controls #
    # Create Control Attributes
    m.addItem(side + '_EndFeathers_CON', longName='GroupControls', defaultValue=0.0, minValue=0.0, maxValue=1.0)
    m.setAttr(side + '_EndFeathers_CON.GroupControls', k=1)  # Make it keyable

    # Key them for on and off
    m.setAttr(side + '_EndFeathers_CON.GroupControls', 0)
    m.setAttr(side + '_MedianCoverts_Con_1.visibility', 0)
    m.setAttr(side + '_Secondaries_Con_1.visibility', 0)
    m.setAttr(side + '_SecondaryCoverts_Con_1.visibility', 0)

    m.setDrivenKeyframe(side + '_MedianCoverts_Con_1.visibility', cd=side + '_EndFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_Secondaries_Con_1.visibility', cd=side + '_EndFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_SecondaryCoverts_Con_1.visibility', cd=side + '_EndFeathers_CON.GroupControls')

    m.setAttr(side + '_EndFeathers_CON.GroupControls', 1)
    m.setAttr(side + '_MedianCoverts_Con_1.visibility', 1)
    m.setAttr(side + '_Secondaries_Con_1.visibility', 1)
    m.setAttr(side + '_SecondaryCoverts_Con_1.visibility', 1)

    m.setDrivenKeyframe(side + '_MedianCoverts_Con_1.visibility', cd=side + '_EndFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_Secondaries_Con_1.visibility', cd=side + '_EndFeathers_CON.GroupControls')
    m.setDrivenKeyframe(side + '_SecondaryCoverts_Con_1.visibility', cd=side + '_EndFeathers_CON.GroupControls')

    # Set controls to default 0 (Invisible)
    m.setAttr(side + '_TipFeathers_CON.GroupControls', 0)
    m.setAttr(side + '_MiddleFeathers_CON.GroupControls', 0)
    m.setAttr(side + '_EndFeathers_CON.GroupControls', 0)

    # Blendshape Controls #
    # Tip Feathers Blendshape Controls #
    # Create Control Attributes
    if (m.objExists(side + '_Primaries_BLND')) or (m.objExists(side + '_Secondaries_BLND')):
        m.addItem(side + '_TipFeathers_CON', longName='FlexControls', defaultValue=0.0, minValue=0.0, maxValue=1.0)
        m.setAttr(side + '_TipFeathers_CON.FlexControls', k=1)  # Make it keyable

        m.setAttr(side + '_TipFeathers_CON.FlexControls', 0)
        m.setAttr(side + '_Tip_Flex_Feathers.visibility', 0)
        m.setDrivenKeyframe(side + '_Tip_Flex_Feathers.visibility', cd=side + '_TipFeathers_CON.FlexControls')
        m.setAttr(side + '_TipFeathers_CON.FlexControls', 1)
        m.setAttr(side + '_Tip_Flex_Feathers.visibility', 1)
        m.setDrivenKeyframe(side + '_Tip_Flex_Feathers.visibility', cd=side + '_TipFeathers_CON.FlexControls')

        # Middle Feathers Blendshape Controls #
        # Create Control Attributes
        m.addItem(side + '_MiddleFeathers_CON', longName='FlexControls', defaultValue=0.0, minValue=0.0, maxValue=1.0)
        m.setAttr(side + '_MiddleFeathers_CON.FlexControls', k=1)  # Make it keyable

        m.setAttr(side + '_MiddleFeathers_CON.FlexControls', 0)
        m.setAttr(side + '_Mid_R_Flex_Feathers.visibility', 0)
        m.setAttr(side + '_Mid_L_Flex_Feathers.visibility', 0)
        m.setDrivenKeyframe(side + '_Mid_R_Flex_Feathers.visibility', cd=side + '_MiddleFeathers_CON.FlexControls')
        m.setDrivenKeyframe(side + '_Mid_L_Flex_Feathers.visibility', cd=side + '_MiddleFeathers_CON.FlexControls')

        m.setAttr(side + '_MiddleFeathers_CON.FlexControls', 1)
        m.setAttr(side + '_Mid_R_Flex_Feathers.visibility', 1)
        m.setAttr(side + '_Mid_L_Flex_Feathers.visibility', 1)
        m.setDrivenKeyframe(side + '_Mid_R_Flex_Feathers.visibility', cd=side + '_MiddleFeathers_CON.FlexControls')
        m.setDrivenKeyframe(side + '_Mid_L_Flex_Feathers.visibility', cd=side + '_MiddleFeathers_CON.FlexControls')

        # End Feathers Blendshape Controls #
        # Create Control Attributes
        m.addItem(side + '_EndFeathers_CON', longName='FlexControls', defaultValue=0.0, minValue=0.0, maxValue=1.0)
        m.setAttr(side + '_EndFeathers_CON.FlexControls', k=1)  # Make it keyable

        m.setAttr(side + '_EndFeathers_CON.FlexControls', 0)
        m.setAttr(side + '_End_Flex_Feathers.visibility', 0)
        m.setDrivenKeyframe(side + '_End_Flex_Feathers.visibility', cd=side + '_EndFeathers_CON.FlexControls')
        m.setAttr(side + '_EndFeathers_CON.FlexControls', 1)
        m.setAttr(side + '_End_Flex_Feathers.visibility', 1)
        m.setDrivenKeyframe(side + '_End_Flex_Feathers.visibility', cd=side + '_EndFeathers_CON.FlexControls')

        # Set controls to default 0 (Invisible)
        m.setAttr(side + '_TipFeathers_CON.FlexControls', 0)
        m.setAttr(side + '_MiddleFeathers_CON.FlexControls', 0)
        m.setAttr(side + '_EndFeathers_CON.FlexControls', 0)

    # Parent Main groups properly
    if ((m.objExists('R_Wing_1_JNT') == 0) and (m.objExists('L_Wing_1_JNT') == 1)) or (
                (m.objExists('R_Wing_1_JNT') == 1) and (m.objExists('L_Wing_1_JNT') == 0)):
        # if only one exists, then parent the joints properly
        m.parent
        m.parent
        m.parent

    m.parent
    m.parent
    m.parent
    m.parent
    # Parent Feather Groups properly
    m.parent
    m.parent
    m.parent
    m.parent
    m.parent
    m.parent

    m.parent  # Function to create the blendshapes for each feather


def makeBlends(featherName, numFeathers):
    NAME = side + featherName
    i = 1

    # While function creates a blendshape for each feather.
    while (i < (numFeathers + 1)):
        m.select(NAME + 'BLND', r=True)
        m.select(NAME + repr(i), tgl=True)

        m.blendShape(n=NAME + repr(i) + '_BLNDSHP')

        i = i + 1


# Function to create the system for the blendshapes.
# Works similarly to the feather controls- each blendshape is keyed in proportionally to it's position in
# the wing.
def blendshapeSys(featherName, numFeathers, control1, control2):
    NAME = side + featherName
    numFeathers = numFeathers
    control1 = control1
    control2 = control2

    i = 1
    stepAmount = 1.0 / numFeathers  # Step incriment for each blendshape- Percentage by number of feathers
    j = stepAmount
    k = 1

    # Create nodes to do the math for the blendshapes
    while (i < (numFeathers + 1)):
        # Create node structure
        m.createNode('multiplyDivide', n=NAME + repr(i) + '_MDNode1')  # creates plus min avg node
        m.createNode('multiplyDivide', n=NAME + repr(i) + '_MDNode2')  # creates plus min avg node
        m.createNode('plusMinusAverage', n=NAME + repr(i) + '_PMNode')  # creates plus min avg node

        # First multiplication- Multiplies the distance control 2 is moved and the blendshape
        m.setAttr(NAME + repr(i) + '_MDNode1.input1X', facingDirection * (-k))
        m.connectAttr(side + control2 + '.translateY', NAME + repr(i) + '_MDNode1.input2X')
        m.connectAttr(NAME + repr(i) + '_MDNode1.outputX', NAME + repr(i) + '_PMNode.input1D[1]')

        # Second Multiplication- Multiplies the distance control 1 is moved and the blendshape
        m.setAttr(NAME + repr(i) + '_MDNode2.input1X', facingDirection * (-j))
        m.connectAttr(side + control1 + '.translateY', NAME + repr(i) + '_MDNode2.input2X')
        m.connectAttr(NAME + repr(i) + '_MDNode2.outputX', NAME + repr(i) + '_PMNode.input1D[2]')

        m.connectAttr(NAME + repr(i) + '_PMNode.output1D',
                      NAME + repr(i) + '_BLNDSHP.' + NAME + 'BLND')  # Add the results

        # Incriment all the variables
        i = i + 1
        j = j + stepAmount
        k = k - stepAmount

    m.select(cl=True)


# Function that creates the wingfold control
def foldControls():
    # Add control Atribute
    m.addItem(side + '_Shoulder_CON', longName='_AutoWingfold', defaultValue=0.0, minValue=0.0, maxValue=10.0)
    m.setAttr(side + '_Shoulder_CON.' + '_AutoWingfold', k=1)  # Make it keyable

    # Temp variables to fix a problem with the _FLG group inheriting variables it shouldn't (Need to fix this, can't find
    # why it's doing this.This is a temporary fix.)
    tempVar1 = m.xform(side + '_Primaries_Con_1_GRP_FLD', ro=True, q=True, os=True)
    tempVar2 = m.xform(side + '_PrimaryCoverts_Con_1_GRP_FLD', ro=True, q=True, os=True)

    # Set the default positions for all the controls. Use the GRP so that it causes no problems with the controls.
    m.setAttr(side + '_Shoulder_CON.' + '_AutoWingfold', 0)
    m.setAttr(side + '_Shoulder_Con_GRP2.rotateX', 0)
    m.setAttr(side + '_Shoulder_Con_GRP2.rotateY', 0)
    m.setAttr(side + '_Shoulder_Con_GRP2.rotateZ', 0)
    m.setAttr(side + '_Wing2_FK_Con_GRP2.rotateX', 0)
    m.setAttr(side + '_Wing2_FK_Con_GRP2.rotateY', 0)
    m.setAttr(side + '_Wing2_FK_Con_GRP2.rotateZ', 0)
    m.setAttr(side + '_Wing3_FK_Con_GRP2.rotateX', 0)
    m.setAttr(side + '_Wing3_FK_Con_GRP2.rotateY', 0)
    m.setAttr(side + '_Wing3_FK_Con_GRP2.rotateZ', 0)

    m.setAttr(side + '_MiddleFeathers_GRP_FLD.rotateX', 0)
    m.setAttr(side + '_MiddleFeathers_GRP_FLD.rotateY', 0)
    m.setAttr(side + '_MiddleFeathers_GRP_FLD.rotateZ', 0)
    m.setAttr(side + '_EndFeathers_GRP_FLD.rotateX', 0)
    m.setAttr(side + '_EndFeathers_GRP_FLD.rotateY', 0)
    m.setAttr(side + '_EndFeathers_GRP_FLD.rotateZ', 0)
    m.setAttr(side + '_TipFeathers_GRP_FLD.rotateX', 0)
    m.setAttr(side + '_TipFeathers_GRP_FLD.rotateY', 0)
    m.setAttr(side + '_TipFeathers_GRP_FLD.rotateZ', 0)

    m.setAttr(side + '_Primaries_Con_1_GRP_FLD.rotateY', tempVar1[1])
    m.setAttr(side + '_Primaries_Con_2_GRP_FLD.rotateY', 0)
    m.setAttr(side + '_PrimaryCoverts_Con_1_GRP_FLD.rotateY', tempVar2[1])
    m.setAttr(side + '_PrimaryCoverts_Con_2_GRP_FLD.rotateY', 0)
    m.setAttr(side + '_Alula_Con_1_GRP_FLD.rotateY', 0)
    m.setAttr(side + '_Alula_Con_2_GRP_FLD.rotateY', 0)

    # Set the driven envKeys for those position
    m.setDrivenKeyframe(side + '_Shoulder_Con_GRP2.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Shoulder_Con_GRP2.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Shoulder_Con_GRP2.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing2_FK_Con_GRP2.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing2_FK_Con_GRP2.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing2_FK_Con_GRP2.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing3_FK_Con_GRP2.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing3_FK_Con_GRP2.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing3_FK_Con_GRP2.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_MiddleFeathers_GRP_FLD.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_MiddleFeathers_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_MiddleFeathers_GRP_FLD.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_TipFeathers_GRP_FLD.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_TipFeathers_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_TipFeathers_GRP_FLD.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_EndFeathers_GRP_FLD.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_EndFeathers_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_EndFeathers_GRP_FLD.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_Primaries_Con_1_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_Primaries_Con_2_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_PrimaryCoverts_Con_1_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_PrimaryCoverts_Con_2_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_Alula_Con_1_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_Alula_Con_2_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')

    # Due to mirroring the joints, the values need to be switched from positive to negative depending on
    # if a side has already been generated.
    if (side == 'R') and (m.objExists('L_Wing_1_JNT') == 0):
        mirrorSwitch = 1
    elif (side == 'L') and (m.objExists('R_Wing_1_JNT') == 0):
        mirrorSwitch = -1
    elif (side == 'R') and (m.objExists('L_Wing_1_JNT') == 1):
        mirrorSwitch = -1
    elif (side == 'L') and (m.objExists('R_Wing_1_JNT') == 1):
        mirrorSwitch = 1

    if (side == "L"):
        # Set the end positions for all the controls. Use the GRP so that it causes no problems with the controls.
        m.setAttr(side + '_Shoulder_CON.' + '_AutoWingfold', 10)
        m.setAttr(side + '_Shoulder_Con_GRP2.rotateX',
                  (mirrorSwitch * 34.482))  # Left first: 37.117   #Right first: -37.117
        m.setAttr(side + '_Shoulder_Con_GRP2.rotateY',
                  (mirrorSwitch * 63.435))  # Left first: -62.464   #Right first: 62.464
        m.setAttr(side + '_Shoulder_Con_GRP2.rotateZ', 52.487)
        m.setAttr(side + '_Wing2_FK_Con_GRP2.rotateX',
                  (mirrorSwitch * 20.614))  # Left first: -20.614       #Right first: 20.614
        m.setAttr(side + '_Wing2_FK_Con_GRP2.rotateY',
                  (mirrorSwitch * -0.579))  # Left first: 0.579   #Right first: -0.579
        m.setAttr(side + '_Wing2_FK_Con_GRP2.rotateZ', 143.43)
        m.setAttr(side + '_Wing3_FK_Con_GRP2.rotateX', 0)
        m.setAttr(side + '_Wing3_FK_Con_GRP2.rotateY',
                  (mirrorSwitch * -8.744))  # Left first: 8.744   #Right first: -8.744
        m.setAttr(side + '_Wing3_FK_Con_GRP2.rotateZ', 134.598)

        m.setAttr(side + '_MiddleFeathers_GRP_FLD.rotateX', -8.84)
        m.setAttr(side + '_MiddleFeathers_GRP_FLD.rotateY', -45.413)
        m.setAttr(side + '_MiddleFeathers_GRP_FLD.rotateZ', 14.6123)
        m.setAttr(side + '_EndFeathers_GRP_FLD.rotateX', 8.925)
        m.setAttr(side + '_EndFeathers_GRP_FLD.rotateY', 38.381)
        m.setAttr(side + '_EndFeathers_GRP_FLD.rotateZ', 12.605)
        m.setAttr(side + '_TipFeathers_GRP_FLD.rotateX', 9.839)
        m.setAttr(side + '_TipFeathers_GRP_FLD.rotateY', 24.161)
        m.setAttr(side + '_TipFeathers_GRP_FLD.rotateZ', -6.711)

        m.setAttr(side + '_Primaries_Con_1_GRP_FLD.rotateY', tempVarPrimary + tempVar1[1])
        m.setAttr(side + '_Primaries_Con_2_GRP_FLD.rotateY', tempVarPrimary2)
        m.setAttr(side + '_PrimaryCoverts_Con_1_GRP_FLD.rotateY', tempVarPrimaryCovert + tempVar2[1])
        m.setAttr(side + '_PrimaryCoverts_Con_2_GRP_FLD.rotateY', tempVarPrimaryCovert2)
        m.setAttr(side + '_Alula_Con_1_GRP_FLD.rotateY', tempVarAlula)
        m.setAttr(side + '_Alula_Con_2_GRP_FLD.rotateY', tempVarAlula2)

    if (side == "R"):
        # Set the default positions for all the controls. Use the GRP so that it causes no problems with the controls.
        m.setAttr(side + '_Shoulder_CON.' + '_AutoWingfold', 10)
        m.setAttr(side + '_Shoulder_Con_GRP2.rotateX',
                  (mirrorSwitch * 34.482))  # Left first: 15.279   #Right first: -15.279
        m.setAttr(side + '_Shoulder_Con_GRP2.rotateY', (mirrorSwitch * 63.435))  # Left first: -82   #Right first: 82
        m.setAttr(side + '_Shoulder_Con_GRP2.rotateZ', 52.487)
        m.setAttr(side + '_Wing2_FK_Con_GRP2.rotateX',
                  (mirrorSwitch * 20.614))  # Left first: -20.614       #Right first: 20.614
        m.setAttr(side + '_Wing2_FK_Con_GRP2.rotateY',
                  (mirrorSwitch * -0.579))  # Left first: 0.579   #Right first: -0.579
        m.setAttr(side + '_Wing2_FK_Con_GRP2.rotateZ', 143.43)
        m.setAttr(side + '_Wing3_FK_Con_GRP2.rotateX', 0)
        m.setAttr(side + '_Wing3_FK_Con_GRP2.rotateY',
                  (mirrorSwitch * -8.744))  # Left first: 8.744   #Right first: -8.744
        m.setAttr(side + '_Wing3_FK_Con_GRP2.rotateZ', 134.598)

        m.setAttr(side + '_MiddleFeathers_GRP_FLD.rotateX', -8.84)
        m.setAttr(side + '_MiddleFeathers_GRP_FLD.rotateY', 45.413)
        m.setAttr(side + '_MiddleFeathers_GRP_FLD.rotateZ', -14.612)
        m.setAttr(side + '_EndFeathers_GRP_FLD.rotateX', 8.925)
        m.setAttr(side + '_EndFeathers_GRP_FLD.rotateY', -38.381)
        m.setAttr(side + '_EndFeathers_GRP_FLD.rotateZ', -12.605)
        m.setAttr(side + '_TipFeathers_GRP_FLD.rotateX', 16.489)
        m.setAttr(side + '_TipFeathers_GRP_FLD.rotateY', -21.683)
        m.setAttr(side + '_TipFeathers_GRP_FLD.rotateZ', -6.06)

        m.setAttr(side + '_Primaries_Con_1_GRP_FLD.rotateY', (-1 * tempVarPrimary) + tempVar1[1])
        m.setAttr(side + '_Primaries_Con_2_GRP_FLD.rotateY', (-1 * tempVarPrimary2))
        m.setAttr(side + '_PrimaryCoverts_Con_1_GRP_FLD.rotateY', (-1 * tempVarPrimaryCovert) + tempVar2[1])
        m.setAttr(side + '_PrimaryCoverts_Con_2_GRP_FLD.rotateY', (-1 * tempVarPrimaryCovert2))
        m.setAttr(side + '_Alula_Con_1_GRP_FLD.rotateY', (-1 * tempVarAlula))
        m.setAttr(side + '_Alula_Con_2_GRP_FLD.rotateY', (-1 * tempVarAlula2))


        # Set the driven envKeys for those position
    m.setDrivenKeyframe(side + '_Shoulder_Con_GRP2.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Shoulder_Con_GRP2.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Shoulder_Con_GRP2.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing2_FK_Con_GRP2.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing2_FK_Con_GRP2.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing2_FK_Con_GRP2.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing3_FK_Con_GRP2.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing3_FK_Con_GRP2.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_Wing3_FK_Con_GRP2.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold', itt='linear',
                        ott='linear')
    m.setDrivenKeyframe(side + '_MiddleFeathers_GRP_FLD.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_MiddleFeathers_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_MiddleFeathers_GRP_FLD.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_TipFeathers_GRP_FLD.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_TipFeathers_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_TipFeathers_GRP_FLD.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_EndFeathers_GRP_FLD.rotateX', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_EndFeathers_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_EndFeathers_GRP_FLD.rotateZ', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_Primaries_Con_1_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_Primaries_Con_2_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_PrimaryCoverts_Con_1_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_PrimaryCoverts_Con_2_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_Alula_Con_1_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')
    m.setDrivenKeyframe(side + '_Alula_Con_2_GRP_FLD.rotateY', cd=side + '_Shoulder_CON.' + '_AutoWingfold',
                        itt='linear', ott='linear')

    m.setAttr(side + '_Shoulder_CON.' + '_AutoWingfold', 0)  # Set the default position to 0


# Function to add color to the controls based on which side they're located on
# Red and light red (pink) for the right, blue and light blue for the left.
def colorControls(controlName, isSubControl):
    # Add color to the main wing Control
    # m.select('MainWing_CON' ) #Select the control
    # Pickwalk down to select the curve so that the parented objects are not also colored, only the control
    # name = m.pickWalk( direction='down')

    m.select(side + controlName)
    # Pickwalk down to select the curve so that the parented objects are not also colored, only the control
    name = m.pickWalk(direction='down')
    name = str(name[0])  # Cast name to a string since pickwalk produces an array

    # Enable Drawing Override
    m.setAttr(name + '.overrideEnabled', 1)

    if (side == 'R'):
        if (isSubControl == 1):
            # If it's a sub control, make it pink,
            m.setAttr(name + '.overrideColor', 20)
        else:
            # Else make it red.
            m.setAttr(name + '.overrideColor', 13)
    elif (side == 'L'):
        if (isSubControl == 1):
            # If it's a sub control, make it pink,
            m.setAttr(name + '.overrideColor', 18)
        else:
            # Blue for the left side
            m.setAttr(name + '.overrideColor', 6)


##Helper functions (Math functions, set functions)
# Mathmatical function to calculate distance between two points since Python doesn't have
# the native vector math that MEL can do *Crys*
def distanceBetweenTwoPoints(value1, value2):
    if isinstance(value1, list) and isinstance(value2, list):
        # Since the wing is flat, we only are doing distance in 2 dimensions, ignoring the Y
        dx = value1[0] - value2[0]
        dz = value1[2] - value2[2]

        distance = math.sqrt((dx * dx) + (dz * dz))
    elif isinstance(value1, float) and isinstance(value2, float):
        distance = abs(value1 - value2)

    return distance


# Function to get locators values once the user presses
def setLocators():
    global Loc1Coord, Loc2Coord, Loc3Coord, Loc4Coord

    Loc1Coord = m.xform(side + '_Wing_1', t=True, q=True, ws=True)  # Shoulder location coordinates
    Loc2Coord = m.xform(side + '_Wing_2', t=True, q=True, ws=True)  # Elbow location coordinates
    Loc3Coord = m.xform(side + '_Wing_3', t=True, q=True, ws=True)  # Wrist location coordinates
    Loc4Coord = m.xform(side + '_Wing_4', t=True, q=True, ws=True)  # Fingertips location coordinates


##Error Checking
# This function checks to make sure the integral parts of the rig are there
# If any are missing it will throw an error and not allow the code to proceed
def existanceCheck():
    global exists
    exists = 1

    # check to see if all the feathers exist
    if (m.objExists('R_Primaries_Base') == 0):
        exists = 0
        print "R Primary missing"

    if (m.objExists('L_Primaries_Base') == 0):
        exists = 0
        print "L Primary missing"

    if (m.objExists('L_PrimaryCoverts_Base') == 0):
        exists = 0
        print "L Primary Covert missing"

    if (m.objExists('R_PrimaryCoverts_Base') == 0):
        exists = 0
        print "R Primary Covert missing"

    if (m.objExists('R_Secondaries_Base') == 0):
        exists = 0
        print "R Secondary missing"

    if (m.objExists('L_Secondaries_Base') == 0):
        exists = 0
        print "L Secondary missing"

    if (m.objExists('R_SecondaryCoverts_Base') == 0):
        exists = 0
        print "R Secondary Coverts missing"

    if (m.objExists('L_SecondaryCoverts_Base') == 0):
        exists = 0
        print "L Secondary Coverts missing"

    if (m.objExists('R_MedianCoverts_Base') == 0):
        exists = 0
        print "R Median Coverts missing"

    if (m.objExists('L_MedianCoverts_Base') == 0):
        exists = 0
        print "L Median Coverts missing"

    if (m.objExists('R_Alula_Base') == 0):
        exists = 0
        print "R Alula missing"

    if (m.objExists('L_Alula_Base') == 0):
        exists = 0
        print "L Alula missing"

        # if (m.objExists('Tertial_Base') == 0):
    # exists = 0
    #   print "Tertial missing"

    # Check Locators
    i = 1
    while (i < 5):
        if (m.objExists(side + '_Wing_' + repr(i)) == 0):
            exists = 0
            print side + '_Wing_' + repr(i) + " missing"

        i = i + 1


# Function to make sure the user hasn't given any numbers that are out of bounds such as 0 or 1.
# The minimum number of feathers is set to three.
def checkUserInput():
    global userInputCheck
    userInputCheck = 1

    if (numPrimaries < 3):
        userInputCheck = 0
        print "Too few Primaries"

    if (numSecondaries < 3):
        userInputCheck = 0
        print "Too few Secondaries"

    if (numPrimaryCoverts < 3):
        userInputCheck = 0
        print "Too few Primary Coverts"

    if (numSecondaryCoverts < 3):
        userInputCheck = 0
        print "Too few Secondary Coverts"

    if (numMedianCoverts < 3):
        userInputCheck = 0
        print "Too few Secondary Coverts"


# Function to check if a given value is a number or a string
def checkNumerical(valueToCheck):
    try:
        float(valueToCheck)
        return 1
    except ValueError:
        return 0


##Cleanup/Finalization
# Function that cleans up any extra stuff that needs to be done such as locking controlers,
# hiding things, locking visibility, deleting extras...
def cleanup():
    i = 0

    # Unhide the main control
    m.showHidden('MainWing_CON')

    # Create array variables for simplicities sake
    scale = [".sx", ".sy", ".sz"]
    translate = [".translateX", ".translateY", ".translateZ"]
    rotate = [".rotateX", ".rotateY", ".rotateZ"]

    while (i < 3):
        # Lock an attribute to prevent further modification on FK controls
        m.setAttr(side + '_Wing2_FK_CON' + scale[i], k=0, lock=True)
        m.setAttr(side + '_Wing2_FK_CON' + translate[i], k=0, lock=True)

        m.setAttr(side + '_Wing3_FK_CON' + scale[i], k=0, lock=True)
        m.setAttr(side + '_Wing3_FK_CON' + translate[i], k=0, lock=True)

        m.setAttr(side + '_Shoulder_CON' + scale[i], lock=True, k=0)
        m.setAttr(side + '_Wrist_CON' + scale[i], lock=True, k=0)

        # Lock spread controls
        m.setAttr(side + '_TipFeathers_CON' + scale[i], lock=True, k=0)
        m.setAttr(side + '_MiddleFeathers_CON' + scale[i], lock=True, k=0)
        m.setAttr(side + '_EndFeathers_CON' + scale[i], lock=True, k=0)
        m.setAttr(side + '_TipFeathers_CON' + translate[i], lock=True, k=0)
        m.setAttr(side + '_MiddleFeathers_CON' + translate[i], lock=True, k=0)
        m.setAttr(side + '_EndFeathers_CON' + translate[i], lock=True, k=0)

        # Lock Flex controls
        if (m.objExists(side + '_Primaries_BLND')) or (m.objExists(side + '_Secondaries_BLND')):
            m.setAttr(side + '_Tip_Flex_Feathers' + rotate[i], lock=True, k=0)
            m.setAttr(side + '_Mid_L_Flex_Feathers' + rotate[i], lock=True, k=0)
            m.setAttr(side + '_Mid_R_Flex_Feathers' + rotate[i], lock=True, k=0)
            m.setAttr(side + '_End_Flex_Feathers' + rotate[i], lock=True, k=0)
            m.setAttr(side + '_Tip_Flex_Feathers' + scale[i], lock=True, k=0)
            m.setAttr(side + '_Mid_L_Flex_Feathers' + scale[i], lock=True, k=0)
            m.setAttr(side + '_Mid_R_Flex_Feathers' + scale[i], lock=True, k=0)
            m.setAttr(side + '_End_Flex_Feathers' + scale[i], lock=True, k=0)

        # Lock Pole vector
        m.setAttr(side + '_Wing_Pole_CON' + scale[i], lock=True, k=0)
        m.setAttr(side + '_Wing_Pole_CON' + rotate[i], lock=True, k=0)

        # Lock low level controls
        m.setAttr(side + '_Primaries_Con_1' + scale[i], lock=True, k=0)
        m.setAttr(side + '_Primaries_Con_1' + translate[i], lock=True, k=0)
        m.setAttr(side + '_Primaries_Con_2' + scale[i], lock=True, k=0)
        m.setAttr(side + '_Primaries_Con_2' + translate[i], lock=True, k=0)
        m.setAttr(side + '_PrimaryCoverts_Con_1' + scale[i], lock=True, k=0)
        m.setAttr(side + '_PrimaryCoverts_Con_1' + translate[i], lock=True, k=0)
        m.setAttr(side + '_PrimaryCoverts_Con_2' + scale[i], lock=True, k=0)
        m.setAttr(side + '_PrimaryCoverts_Con_2' + translate[i], lock=True, k=0)

        m.setAttr(side + '_Secondaries_Con_1' + scale[i], lock=True, k=0)
        m.setAttr(side + '_Secondaries_Con_1' + translate[i], lock=True, k=0)
        m.setAttr(side + '_Secondaries_Con_2' + scale[i], lock=True, k=0)
        m.setAttr(side + '_Secondaries_Con_2' + translate[i], lock=True, k=0)
        m.setAttr(side + '_SecondaryCoverts_Con_1' + scale[i], lock=True, k=0)
        m.setAttr(side + '_SecondaryCoverts_Con_1' + translate[i], lock=True, k=0)
        m.setAttr(side + '_SecondaryCoverts_Con_2' + scale[i], lock=True, k=0)
        m.setAttr(side + '_SecondaryCoverts_Con_2' + translate[i], lock=True, k=0)

        m.setAttr(side + '_MedianCoverts_Con_1' + scale[i], lock=True, k=0)
        m.setAttr(side + '_MedianCoverts_Con_1' + translate[i], lock=True, k=0)
        m.setAttr(side + '_MedianCoverts_Con_2' + scale[i], lock=True, k=0)
        m.setAttr(side + '_MedianCoverts_Con_2' + translate[i], lock=True, k=0)

        m.setAttr(side + '_Alula_Con_1' + scale[i], lock=True, k=0)
        m.setAttr(side + '_Alula_Con_1' + translate[i], lock=True, k=0)

        i = i + 1

    m.setAttr(side + '_Wing_1_JNT.visibility', 0)  # Turn off visibility for the main joint set
    m.setAttr(side + '_Wing_IK.visibility', 0)  # Turn off visibility for the IK

    # lock visibility on feather controls
    m.setAttr(side + '_MedianCoverts_Con_1.visibility', lock=True, k=0)
    m.setAttr(side + '_MedianCoverts_Con_2.visibility', lock=True, k=0)
    m.setAttr(side + '_SecondaryCoverts_Con_1.visibility', lock=True, k=0)
    m.setAttr(side + '_SecondaryCoverts_Con_2.visibility', lock=True, k=0)
    m.setAttr(side + '_Secondaries_Con_1.visibility', lock=True, k=0)
    m.setAttr(side + '_Secondaries_Con_2.visibility', lock=True, k=0)
    m.setAttr(side + '_PrimaryCoverts_Con_1.visibility', lock=True, k=0)
    m.setAttr(side + '_PrimaryCoverts_Con_2.visibility', lock=True, k=0)
    m.setAttr(side + '_Primaries_Con_1.visibility', lock=True, k=0)
    m.setAttr(side + '_Primaries_Con_2.visibility', lock=True, k=0)
    m.setAttr(side + '_Alula_Con_1.visibility', lock=True, k=0)
    m.setAttr(side + '_Alula_Con_2.visibility', lock=True, k=0)

    # Lock Flex controls and visibility on flex controls
    if (m.objExists(side + '_Primaries_BLND')) or (m.objExists(side + '_Secondaries_BLND')):
        m.setAttr(side + '_Tip_Flex_Feathers.translateX', lock=True, k=0)
        m.setAttr(side + '_Mid_L_Flex_Feathers.translateX', lock=True, k=0)
        m.setAttr(side + '_Mid_R_Flex_Feathers.translateX', lock=True, k=0)
        m.setAttr(side + '_Tip_Flex_Feathers.translateZ', lock=True, k=0)
        m.setAttr(side + '_Mid_L_Flex_Feathers.translateZ', lock=True, k=0)
        m.setAttr(side + '_Mid_R_Flex_Feathers.translateZ', lock=True, k=0)
        m.setAttr(side + '_End_Flex_Feathers.translateX', lock=True, k=0)
        m.setAttr(side + '_End_Flex_Feathers.translateZ', lock=True, k=0)
        m.setAttr(side + '_Tip_Flex_Feathers.visibility', lock=True, k=0)
        m.setAttr(side + '_Mid_L_Flex_Feathers.visibility', lock=True, k=0)
        m.setAttr(side + '_Mid_R_Flex_Feathers.visibility', lock=True, k=0)
        m.setAttr(side + '_End_Flex_Feathers.visibility', lock=True, k=0)

        if (side == "L"):
            m.setAttr(side + '_Mid_R_Flex_Feathers.translateZ', lock=True, k=0)
        if (side == "R"):
            m.setAttr(side + '_Mid_L_Flex_Feathers.translateZ', lock=True, k=0)

        # Set Limits on Feather curl
        m.select(side + '_Tip_Flex_Feathers')
        m.transformLimits(ty=(-1.3, 1.3), ety=(True, True))
        m.select(side + '_Mid_L_Flex_Feathers')
        m.transformLimits(ty=(-1.3, 1.3), ety=(True, True))
        m.select(side + '_Mid_R_Flex_Feathers')
        m.transformLimits(ty=(-1.3, 1.3), ety=(True, True))
        m.select(side + '_End_Flex_Feathers')
        m.transformLimits(ty=(-1.3, 1.3), ety=(True, True))
    # Delete extraneous
    i = 1
    while (i < 5):
        m.delete(side + '_Wing_' + repr(i))
        i = i + 1

    # If the motion system function has been run, delete the extraneous bases
    if m.objExists('L_Wrist_CON'):
        if m.objExists('R_Wrist_CON'):
            m.delete('L_Primaries_Base')
            m.delete('R_Primaries_Base')
            m.delete('L_Secondaries_Base')
            m.delete('R_Secondaries_Base')
            m.delete('R_PrimaryCoverts_Base')
            m.delete('L_PrimaryCoverts_Base')
            m.delete('R_SecondaryCoverts_Base')
            m.delete('L_SecondaryCoverts_Base')
            m.delete('R_MedianCoverts_Base')
            m.delete('L_MedianCoverts_Base')
            m.delete('R_Alula_Base')
            m.delete('L_Alula_Base')
            # m.delete('Tertial_Base')

    # Delete the base controllers
    m.delete('CONBASE')
    m.delete('BoxConBase')
    m.delete('ArrowConBase')
    m.delete('MoveAllConBase')
    m.delete('CurveConBase')

    # delete extra IK that got duplicated upon mirroring the IK chain. IK is added later in the code.
    if m.objExists('L_Wing_IK1'): m.delete('L_Wing_IK1')
    if m.objExists('R_Wing_IK1'): m.delete('R_Wing_IK1')

    m.select(cl=True)


##GUI and GUI Functions
# Class defining the user interface
class ui():
    def __init__(self, winName="winTheWindow"):
        self.winTitle = "Wing Generator"
        self.winName = winName

    # Create the GUI
    def create(self):
        # if an instance of the window already exists, delete it
        if m.window(self.winName, exists=True):
            m.deleteUI(self.winName)

        # Make the window and setup the columns
        m.window(self.winName, title=self.winTitle)

        form = m.formLayout()
        # Set the layout as a tab layout
        tabs = m.tabLayout(innerMarginWidth=5, innerMarginHeight=5, height=335, width=300)

        m.formLayout(form, edit=True,
                     attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)))

        ##First Tab
        tab1 = m.columnLayout(adjustableColumn=False)
        m.separator(h=15, style='none')
        # Add the text fields for the feather groups
        m.textFieldGrp("textGroup1", label='Primaries', editable=True, text="10", width=200)
        m.textFieldGrp("textGroup2", label='Secondaries', editable=True, text="13", width=200)
        m.textFieldGrp("textGroup3", label='Primary Coverts', editable=True, text="10", width=200)
        m.textFieldGrp("textGroup4", label='Secondary Coverts', editable=True, text="13", width=200)
        m.textFieldGrp("textGroup5", label='Median Coverts', editable=True, text="13", width=200)

        m.separator(h=15, style='none')

        # Radio button for the right and left side option
        m.radioButtonGrp("radioSide", label='Chose Side', labelArray2=['Right', 'Left'], numberOfRadioButtons=2,
                         vr=True, select=1)
        m.separator(h=5, style='none')
        # Radio button for the direction the character is facing
        m.radioButtonGrp("radioFacingDirection", label='Character faces down:',
                         labelArray2=['Positive Z', 'Negative Z'], numberOfRadioButtons=2, vr=True, select=1)

        m.separator(h=15, style='none')

        m.rowLayout(numberOfColumns=5, columnWidth5=(10, 70, 70, 70, 10))
        m.text(label='  ')  # Blank text field to help align buttons nicely
        m.button(label='Import Base', c=self.importWingBase, width=70)
        m.button(label='Generate Feathers', c=self.generateButtonFunction, width=70)
        m.button(label='Generate Rig', c=self.motionSysButtonFunction, width=70)
        m.text(label='  ')

        m.setParent('..')
        m.setParent('..')

        ##Second Tab
        tab2 = m.columnLayout(adjustableColumn=False)
        m.separator(h=15, style='none')

        # Radio button for the right and left side option
        m.radioButtonGrp("radioWingType", label='Chose wing shape:  ', labelArray2=['Hawk', 'Falcon'],
                         numberOfRadioButtons=2, vr=True, select=1)

        # Make tab layout with two tabs, one for the rigging stuff, one for the different wing types
        m.tabLayout(tabs, edit=True, tabLabel=((tab1, 'Wing Rig'), (tab2, 'Wing Types')))

        # initiate the window
        m.showWindow(self.winName)
        m.window(self.winName, edit=True, widthHeight=[300, 335])

    def importWingBase(self, *args):
        wingBaseFile = os.path.join(os.getenv('PIPELINE_TOOL'), 'maya', 'plt_modules', 'MayaLib', 'wingBase.ma')

        namespace = 'wingBase'

        m.file(wingBaseFile, i=True, type="mayaAscii", ignoreVersion=True, ra=True, mergeNamespacesOnClash=False,
               namespace=namespace)

        m.namespace(mnr=True, rm=namespace)

    def generateButtonFunction(self, arg=None):
        self.setSide()
        self.setFields()
        self.setWingType()

        if self.setFields() == 0:
            print "Generate feathers aborted, check script editor for details."
        elif self.setFields() == 1:
            generateFeathers()

    def motionSysButtonFunction(self, args=None):
        self.setSide()

        generateMotionSys()

    def setWingType(self, args=None):
        global wingType

        self.radio3 = m.radioButtonGrp("radioWingType", query=True, sl=1)

        # Set Wing Type
        if (self.radio3 == 1):
            wingType = 0
        elif (self.radio3 == 2):
            wingType = 1
        else:
            wingType = 0  # Default is hawk wing

    def setSide(self, arg=None):
        global side

        self.radio1 = m.radioButtonGrp("radioSide", query=True, sl=1)

        # Set side
        if (self.radio1 == 1):
            side = 'R'
        elif (self.radio1 == 2):
            side = 'L'
        else:
            self.sideChosen = 'R'  # Default is right side

    # Function to get the information from the text fields and save them to a value
    def setFields(self, arg=None):
        # Set variables
        global facingDirection
        global numPrimaries
        global numSecondaries
        global numPrimaryCoverts
        global numSecondaryCoverts
        global numMedianCoverts
        global numAlulas

        # global numTertials

        self.radio2 = m.radioButtonGrp("radioFacingDirection", query=True, sl=1)

        # Set Direction the characer is facing,
        # 1 = positive Z (industry standard), 2 = negative Z
        # NOTE: When I made this script I made it -backwards-. I had the character facing negative z instead of positive z.  Therefore facing direction
        # is -1 by default, so that all my functions multiply by a negative therefore reversing everything for the standard character facing positive Z.
        # For a character facing negative z, facing direction changes to 1.
        if (self.radio2 == 1):
            facingDirection = -1
        elif (self.radio2 == 2):
            facingDirection = 1
        else:
            facingDirection = -1

        # Set the values for the text fields and radio buttons
        numPrimaries = m.textFieldGrp("textGroup1", query=True, text=True)
        numSecondaries = m.textFieldGrp("textGroup2", query=True, text=True)
        numPrimaryCoverts = m.textFieldGrp("textGroup3", query=True, text=True)
        numSecondaryCoverts = m.textFieldGrp("textGroup4", query=True, text=True)
        numMedianCoverts = m.textFieldGrp("textGroup5", query=True, text=True)

        # Check to make sure values are actual numbers and not something invalid (a string)
        if checkNumerical(numPrimaries) == 0:
            print 'Primaries must be a numerical value, strings not allowed.'
        elif checkNumerical(numSecondaries) == 0:
            print 'Secondaries must be a numerical value, strings not allowed.'
        elif checkNumerical(numPrimaryCoverts) == 0:
            print 'Primary Coverts must be a numerical value, strings not allowed.'
        elif checkNumerical(numSecondaryCoverts) == 0:
            print 'Secondary Coverts must be a numerical value, strings not allowed.'
        elif checkNumerical(numMedianCoverts) == 0:
            print 'Median Coverts must be a numerical value, strings not allowed.'
        else:
            # If they're correct, cast them to floats
            numPrimaries = float(numPrimaries)
            numSecondaries = float(numSecondaries)
            numPrimaryCoverts = float(numPrimaryCoverts)
            numSecondaryCoverts = float(numSecondaryCoverts)
            numMedianCoverts = float(numMedianCoverts)
            return 1


# GUI button function 1
# Call the generation functions when the button to generate feathers is pressed
def generateFeathers():
    # Check to make sure function hasn't been run yet by checking to see if the first feather exists
    if (m.objExists(side + '_Primaries_1') == 0):
        existanceCheck()  # check to make sure all objects needed for the program are there

        if (exists == 1):  # If all objects are there, now check the users input to make sure it's within bounds
            checkUserInput()

            if (userInputCheck == 1):
                # check to see if startup function has been run by checking the existance of the controls group
                if m.objExists('WingControls'):
                    print "Startup already run. Skipping."
                else:
                    runAtStartup()
                    print "Startup complete."

                print "All parts accounted for, generating feathers."

                # set the locators for the joint positions
                setLocators()

                # Run feather generation functions
                my_wing.buildFeathers("_Primaries_", numPrimaries, 10.0, Loc4Coord, Loc3Coord)
                my_wing.buildFeathers("_PrimaryCoverts_", numPrimaryCoverts, 10.0, Loc4Coord, Loc3Coord)
                my_wing.buildFeathers("_Secondaries_", numSecondaries, 13.0, Loc3Coord, Loc2Coord)
                my_wing.buildFeathers("_SecondaryCoverts_", numSecondaryCoverts, 13.0, Loc3Coord, Loc2Coord)
                my_wing.buildFeathers("_MedianCoverts_", numMedianCoverts, 13.0, Loc3Coord, Loc2Coord)
                my_wing.buildFeathers("_Alula_", numAlulas, 4.0, Loc4Coord, Loc3Coord)
        else:
            print "Cannot generate feathers: Missing integral parts. Check Script Editor for details."
    else:
        print "Feathers have already been generated for this side."


# GUI button function 2
# Call the generation functions when the button to generate the motion system is pressed
def generateMotionSys():
    if (m.objExists(side + '_Primaries_1') == 1):  # make sure feathers have been made
        # Check to make sure function hasn't been run yet by checking to see if the Wrist Control exists
        if (m.objExists(side + '_Wrist_CON') == 0):
            setLocators()
            createWingControls()  # Create the controls
            generateSkeleton()  # Create the skeleton
            controlsSetup()  # now build the controls

            # Setup each of the groups of feathers
            my_wing.featherSetup('_Primaries_', numPrimaries, 'Con_1', 'Con_2', '_Wing_3_JNT')
            my_wing.featherSetup('_Secondaries_', numSecondaries, 'Con_1', 'Con_2', '_Wing_2_JNT')
            my_wing.featherSetup('_PrimaryCoverts_', numPrimaryCoverts, 'Con_1', 'Con_2', '_Wing_3_JNT')
            my_wing.featherSetup('_SecondaryCoverts_', numSecondaryCoverts, 'Con_1', 'Con_2', '_Wing_2_JNT')
            my_wing.featherSetup('_MedianCoverts_', numMedianCoverts, 'Con_1', 'Con_2', '_Wing_2_JNT')
            my_wing.featherSetup('_Alula_', numAlulas, 'Con_1', 'Con_2', '_Wing_3_JNT')

            mainControls()  # Setup the main controls

            if (m.objExists(side + '_Primaries_BLND')):
                # Create blendshape controls on the primary feathers
                makeBlends('_Primaries_', numPrimaries)
                blendshapeSys('_Primaries_', numPrimaries, '_Tip_Flex_Feathers', '_Mid_L_Flex_Feathers')
                print side + " Primary flex Added."
            else:
                print side + " Primary Blendshape missing. Didn't add primary feather flex."

            if (m.objExists(side + '_Secondaries_BLND')):
                # Create blendshape controls on the secondary feathers
                makeBlends('_Secondaries_', numSecondaries)
                blendshapeSys('_Secondaries_', numSecondaries, '_End_Flex_Feathers', '_Mid_R_Flex_Feathers')
                print side + " Secondary flex Added."
            else:
                print side + " Secondary Blendshape missing. Didn't add secondary feather flex."

            foldControls()  # Create controls for wingfolding

            cleanup()  # Run cleanup
            print side + " Motion system generated."
        else:
            print "Motion system already created for this side."
    else:
        print "Cannot generate motion system without feathers. Please generate feathers first."


# Main function call to start the program
def wingCreator():
    # create the window
    inst = ui()
    inst.create()
