# -*- coding: utf-8 -*-
"""

Script Name: _doc.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script is master file of Pipeline Tool

"""

TRADE_MARK = '™'

PLM_ABOUT = """

    PIPELINE MANAGER TO MAKE A SHORT FILM

    This application is built to handle and manage productions as a pipeline tool.
    Currently, it is working with software package: maya, ZBrush, mari, nuke with V-ray plugin.

    The largest version of Python is Python 3.5, however Python 3.x has introduced many breaking changes to Python. 
    These changes are for the better but due to large investment into Python 2 code, maya will continue to be on 
    Python 2 for a while longer.

    You can see the details off platforms that is agreed by industry: www.vfxplatform.com.

    For feedback or questions, feel free to email me: damgteam@gmail.com or dot@damgteam.com

"""


WAIT_FOR_UPDATE = """

this function is currenly under construction, please wait for next update.             
JimJim  

"""

WAIT_TO_COMPLETE = "This function is not completed yet. Please try again later"

WAIT_LAYOUT_COMPLETE = "Udating..."

PASSWORD_FORGOTTON = """

How the hell you forgot your password? Make a showLayout_new one now!!!
(This function will be update soon.)

"""

SIGNUP = "Do not have account?"

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

PTH_NOT_EXSIST = "Could not find directory path specific"

ERROR_OPENFILE = "There was an error opening the file"

ERROR_QIMAGE = "ImageViewer.setImage: Argument must be a QImage or QPixmap."

# what to present when the user hovers the cells
tooltips_present = [ "When the message was sent", "The text of the message (double click to copy to the clipboard)",
                     "The media (image, audio, etc) included in the message",
                     "Select to remove the message from the system", ]

tooltips_missing = [
    None,
    "No text included in the message",
    "No media included in the message",
    None,
]

N_MESSAGES_TEXT = "{quantity} showLayout_new messages"

SERVER_CONNECT_FAIL = "Connection to server failed. PLM can not run without connecting to server. Please try again "

TEMPLATE_QRC_HEADER = '''
<RCC warning="File created programmatically. All changes made in this file will be lost!">
  <qresource prefix="{resource_prefix}">
'''

TEMPLATE_QRC_FILE = '    <file>rc/{fname}</file>'

TEMPLATE_QRC_FOOTER = '''
  </qresource>
  <qresource prefix="{style_prefix}">
      <file>style.qss</file>
  </qresource>
</RCC>
'''

HEADER_SCSS = '''// ---------------------------------------------------------------------------
//
//    File created programmatically
//
//    WARNING! All changes made in this file will be lost!
//
//----------------------------------------------------------------------------
'''

HEADER_QSS = '''/* ---------------------------------------------------------------------------

    Created by the qtsass compiler

    WARNING! All changes made in this file will be lost!

--------------------------------------------------------------------------- */
'''

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 23/10/2019 - 2:48 AM
# © 2017 - 2018 DAMGteam. All rights reserved