#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: subData.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os
from appData.scr._path import CONFIG_DIR

# --------------------------------------------------------------------------------------------------------------
""" Autodesk config """

autodeskVer = ["2017", "2018", "2019", "2020"]

autodeskApp = ["Autodesk Maya", "Autodesk MudBox", "Autodesk 3ds Max", "Autodesk AutoCAD"]

userMayaDir = os.path.expanduser(r"~/Documents/maya")

# --------------------------------------------------------------------------------------------------------------
""" Adobe config """

adobeVer = ["CC 2017", "CC 2018", "CC 2019", ]

adobeApp = ["Adobe Photoshop", "Adobe Illustrator", "Adobe Audition", "Adobe After Effects", "Adobe Premiere Pro",
            "Adobe Media Encoder", ]

# --------------------------------------------------------------------------------------------------------------
""" Foundry config """

foundryVer = ["11.1v1", "11.2v1", "4.0v1", "4.1v1", "2.6v3"]

foundryApp = ['Hiero', 'HieroPlayer', 'Mari', 'NukeX', 'Katana',]

# --------------------------------------------------------------------------------------------------------------
""" Pixologic config """

pixologiVer = ["4R6", "4R7", "4R8"]

pixologiApp = ['ZBrush', ]

# --------------------------------------------------------------------------------------------------------------
""" Allegorithmic config """

allegorithmicVer = []

allegorithmicApp = ['Substance Painter', 'Substance Designer']

# --------------------------------------------------------------------------------------------------------------
""" SideFX config """

sizefxVer = ['16.5.439', '16.5.496']

sizefxApp = ['Houdini FX', ]

# --------------------------------------------------------------------------------------------------------------
""" Microsoft Office config """

officeVer = ['2013', '2015', '2016', '2017']

officeApp = ['Word', 'Excel', 'PowerPoint', 'Wordpad', 'TextEditor', 'NoteReminder']

# --------------------------------------------------------------------------------------------------------------
""" JetBrains config """

jetbrainsVer = ['2017.3.3', '2018.1', ]

jetbrainsApp = ['JetBrains PyCharm', ]
# --------------------------------------------------------------------------------------------------------------
""" Wonder Unit """

wonderUnitVer = []

wonderUniApp = ['Storyboarder']

# --------------------------------------------------------------------------------------------------------------
""" another app config """

anacondaApp = ['Spyder', 'QtDesigner', 'Git Bash']

otherApp = ['Sublime Text 2', 'Sublime Text 3', 'Wordpad', 'Headus UVLayout', 'Snipping Tool', ]

CONFIG_APPUI = ['About', 'Calculator', 'Calendar', 'Credit', 'EnglishDictionary', 'FindFiles', 'ForgotPassword',
                'ImageViewer', 'NewProject', 'Preferences', 'Screenshot', 'UserSetting', 'PLMBrowser', 'NoteReminder',
                'TextEditor', 'NodeGraph']

# --------------------------------------------------------------------------------------------------------------
""" Tracking key """

TRACK_TDS = ['Maya', 'ZBrush', 'Mari', 'Houdini', 'Painter', ]

TRACK_VFX = ['NukeX', 'Davinci Resolve', 'Hiero', 'HieroPlayer', 'After Effects', 'Premiere Pro', 'Media Encoder',]

TRACK_ART = ['Photoshop', 'Illustrator', 'Storyboarder']

TRACK_OFFICE = ['Word', 'Excel', 'PowerPoint', 'Wordpad']

TRACK_DEV = ['PyCharm', 'Sublime Text', 'QtDesigner', 'Git Bash', 'Command Prompt', 'Spyder']

TRACK_TOOLS = ['Calculator', 'Calendar', 'EnglishDictionary', 'FindFiles', 'ImageViewer', 'Screenshot', 'NodeGraph']

TRACK_EXTRA = ['3Ds Max', 'Mudbox', 'BLender', ]

TRACK_SYSTRAY = ['Snipping Tool', 'Screenshot', 'Maximize', 'Minimize', 'Restore', 'Quit', ]

KEYDETECT = ["Non-commercial", "Uninstall", "Verbose", "License", "Skype", ".url"]

FIX_KEY = {'Screenshot': 'screenShot', 'Snipping Tool': 'SnippingTool'}

# --------------------------------------------------------------------------------------------------------------
""" Combine config data """

pVERSION = dict(adobe=adobeVer, autodesk=autodeskVer, allegorithmic = allegorithmicVer, foundry=foundryVer,
                pixologic=pixologiVer, sizefx=sizefxVer, office=officeVer, jetbrains=jetbrainsVer, wonderUnit=wonderUnitVer, )

pPACKAGE = dict(adobe=adobeApp, autodesk=autodeskApp, allegorithmic = allegorithmicApp, foundry=foundryApp,
                pixologic=pixologiApp, sizefx=sizefxApp, office=officeApp, jetbrains=jetbrainsApp, wonderUnit=wonderUniApp,)

pTRACK = dict(TDS=TRACK_TDS, VFX=TRACK_VFX, ART=TRACK_ART, Office=TRACK_OFFICE, Dev=TRACK_DEV,
              Tools=TRACK_TOOLS, Extra=TRACK_EXTRA, sysTray=TRACK_SYSTRAY, )

# --------------------------------------------------------------------------------------------------------------
""" Store config data """

def generate_key_packages(*args):
    keyPackage = []
    for k in pPACKAGE:
        for name in pPACKAGE[k]:
            if len(pVERSION[k]) == 0:
                key = name
                keyPackage.append(key)
            else:
                for ver in pVERSION[k]:
                    if name == 'Hiero' or name == 'HieroPlayer' or name == 'NukeX':
                        key = name + ver
                    else:
                        if not ver or ver == []:
                            key = name
                        else:
                            key = name + " " + ver
                    keyPackage.append(key)

    return keyPackage + otherApp + anacondaApp + CONFIG_APPUI + ['Word', 'Excel', 'PowerPoint']

def generate_config(key, *args):
    keyPackages = generate_key_packages()
    keys = []
    for k in keyPackages:
        for t in pTRACK[key]:
            if t in k:
                keys.append(k)
    return list(sorted(set(keys)))

KEYPACKAGE = generate_key_packages()

# Toolbar config
CONFIG_TDS = generate_config('TDS')
CONFIG_VFX = generate_config('VFX')
CONFIG_ART = generate_config('ART')

# Tab 1 sections config
CONFIG_OFFICE = generate_config('Office')
CONFIG_DEV = generate_config('Dev') + ['Command Prompt']
CONFIG_TOOLS = generate_config('Tools')
CONFIG_EXTRA = generate_config('Extra')
CONFIG_SYSTRAY = generate_config('sysTray')

FILEPATH = os.path.join(CONFIG_DIR, "PLM.cfg")

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/05/2018 - 9:47 AM