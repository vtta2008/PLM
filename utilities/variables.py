#!/usr/bin/env python3
# coding=utf-8
"""

Script Name: variables.py
Author: Do Trinh/Jimmy - 3D artist, pipelineTD artist.

Description:
    This place is a storage of variables

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
# print("Import from modules: {file}".format(file=__name__))
# print("Directory: {path}".format(path=__file__.split(__name__)[0]))
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import logging
import os
import platform

# Plt tools
import appData as app
from utilities import message as mess


# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """

logPth = os.path.join(os.getenv(app.__envKey__), "appData", "logs", "variables.log")
logger = logging.getLogger("variables")
handler = logging.FileHandler(logPth)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# -------------------------------------------------------------------------------------------------------------
""" Variables """

# encode.py
STRINPUT = "password"
HEXINPUT = "70617373776F7264"
ENCODE = ["hexadecimal", "ascii", "unicode"]
OPERATION = dict(encode=["hex", "string"], pathInfo=["create", "read", "modify"])

DEMODATA = ["demoUser", "70617373776F7264", "Mr.", "Nobody", "Homeless", "dot@damgteam.com", "1234567890", "forever",
            "homeless", "no postal", "anywhere", "in the world"]

# Setting Path
UI_SETTING = os.path.join(os.getenv(app.__envKey__), "appData", "settings", "plt.ini")

USER_SETTING = os.path.join(os.getenv(app.__envKey__), "appData", "settings", "User.ini")

DB_PATH = os.path.join(os.getenv(app.__envKey__), "appData", "plt.db")

# getData.py
USER_CLASS = ["", "Admin", "Supervisor", "Artist", "Tester"]

USERNAME = platform.node()

PLT_ID = dict(Main="Pipeline Tool", LogIn="Log in", About="About Pipeline Tool", Credit="From Author")

PLT_TABID = ["", "User", "Functions", "Project", "Admin", ]

PLT_URL = dict(Home = "https://www.dot.damgteam.com/", Help = "https://www.dot.damgteam.com/")

PLT_MESS = dict(About=mess.PLT_ABOUT, Credit=mess.PLT_CREDIT, status="Pipeline Application", )

PLT_PKG = dict(
    TD=["Maya", "3ds Max", "Mudbox", "Houdini FX", "ZBrush", "Mari", "Substance Painter"],
    Comp=["NukeX", "Hiero", "After Effects", "Premiere Pro"],
    Design=["Photoshop", "Illustrator"],
    Microsoft=["Word", "Excel", "Snipping Tool"],
    UV=["UVLayout"],
    Sound=["Audition"],
    Plt=["Git Bash", "Git CMD", "Advance Rename"],
    Dev=["PyCharm", "Sublime Text", "QtDesigner"],

    main = ["Maya", "3ds Max", "Mudbox", "Houdini FX", "ZBrush", "Mari", "Substance Painter", "NukeX", "Hiero", 
            "After Effects", "Premiere Pro", "Photoshop", "Illustrator", "Word", "Excel", "Snipping Tool", "UVLayout",
            "Audition", "Git Bash", "Git CMD", "Advance Rename", "PyCharm", "Sublime Text", "QtDesigner"],

    sysOpts=["Host Name", "Product ID", "System Manufacturer", "System Model", "System type", "BIOS Version", "Domain",
             "Windows Directory", "Total Physical Memory", "Available Physical Memory", "Logon Server"],
    detect=["Non-commercial", "Uninstall", "Verbose", "License", "Skype"],
    py = ["utilities","ui"],
    ext=[".exe", ".lnk"],
)

LLINE = "==============================================================================================================="