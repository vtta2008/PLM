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

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """

logPth = os.path.join(app.LOGPTH)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
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

