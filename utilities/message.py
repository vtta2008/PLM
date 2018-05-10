#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: plt.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
print("Import from modules: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))
# -------------------------------------------------------------------------------------------------------------

PLT_ABOUT = """

PIPELINE TOOL TO MAKE A SHORT FILM

This application is built to handle and manage productions as a pipeline tool.
Currently, it is working with software package: maya, ZBrush, mari, nuke with V-ray plugin.

The largest version of Python is Python 3.5, however Python 3.x has introduced many breaking changes to Python. 
These changes are for the better but due to large investment into Python 2 code, maya will continue to be on 
Python 2 for a while longer.

You can see the details off platforms that is agreed by industry: www.vfxplatform.com.

For feedback or questions, feel free to email me: damgteam@gmail.com or dot@damgteam.com

"""

PLT_CREDIT = """

Special thank to lectures and students in Media Design School:

    Lecture:
        Oliver Hilbert
        Brian Samuel
        Kelly Bechtle-Woods

    Students:
        Brandon Hayman

big thank to DAMG team's members

        Duong Minh Duc - Interactive Media Artist
        Tran Huyen Trang - 2D artist

Also thank to:

        Dhruv Govil, Ardit Sulce, Vasandkumar Kunasekaran - from udemy.com
        
"""

WAIT_FOR_UPDATE = """

this function is currenly under construction, please wait for next update.             
JimJim  

"""

PASSWORD_FORGOTTON = """

How the hell you forgot your password? Make a new one now!!!
(This function will be update soon.)

"""

SIGN_UP = "Do not have account?"

DISALLOW = "Sorry, but only Admin can do this function, please contact JimJim for details."
TIT_BLANK = 'Blank title will be set to "Tester"'

PW_BLANK = "Password must not be blank."
PW_WRONG = "Wrong username or password."
PW_UNMATCH = "Password doesn't match"
PW_CHANGED = "Your password has changed"

FN_BLANK = "Firstname must not be blank"
LN_BLANK = "Lastname must not be blank"
SEC_BLANK = " section should not be blank."

USER_CHECK_REQUIRED = "I agree to the DAMG Terms of Service"
USER_NOT_CHECK = "You must agree with DAMG team term of service"
USER_BLANK = "Username must not be blank."
USER_CHECK_FAIL = "Wrong username or password"
USER_NOT_EXSIST = "The username does not exists"
USER_CONDITION = "This username is under condition and can not log in, please contact to admin."

SYSTRAY_UNAVAI = "Systray could not detect any system tray on this system"