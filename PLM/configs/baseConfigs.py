# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import pprint


class Cfg(dict):

    key                                 = 'ConfigBase'

    def __init__(self):
        dict.__init__(self)

    def print(self):
        pprint.pprint(self)

    def add(self, key, value):
        self[key]                   = value



class Cmds(dict):

    key                             = 'Cmds'

    def __init__(self, key=None, icon=None, tooltip=None, statustip=None,
                       value=None, valueType=None, arg=None, code=None):
        super(Cmds, self).__init__()

        self.key                    = key
        self.icon                   = icon
        self.toolTip                = tooltip
        self.statusTip              = statustip
        self.value                  = value
        self.valueType              = valueType
        self.arg                    = arg
        self.code                   = code

        ks = ['key', 'icon', 'tooltip', 'statustip', 'value', 'valueType', 'arg', 'code']
        vs = [key, icon, tooltip, statustip, value, valueType, arg, code]

        for i in range(len(ks)):
            self[ks[i]]             = vs[i]

        self.update()


class TrackKeys(Cfg):

    key                             = 'TrackKeys'

    TRACK_ART = ['Photoshop', 'Illustrator', 'Krita (x64)', 'Krita (x32)']

    KEYDETECT = ["Non-commercial", "Uninstall", "Verbose", "License", "Skype", ".url", "Changelog", "Settings"]


    pTRACK   = dict(TDS             = ['Maya', 'ZBrush', 'Houdini', '3Ds Max', 'Mudbox', 'BLender'],
                    VFX             = ['NukeX', 'After Effects', 'Katana'],
                    ART             = ['Photoshop', 'Illustrator', 'Krita (x64)', 'Krita (x32)'],
                    PRE             = ['Storyboarder', 'Illustrator'],
                    TEXTURE         = ['Mari', 'Substance Painter'] + TRACK_ART,
                    POST            = ['Davinci Resolve', 'Hiero', 'HieroPlayer', 'Premiere Pro', 'NukeStudio'],
                    Office          = ['Word', 'Excel', 'PowerPoint', 'Wordpad'],
                    Dev             = ['Sublime Text', 'QtDesigner', 'Git Bash', 'Command Prompt'],
                    Tools           = ['Calculator', 'Calendar', 'ContactUs', 'EnglishDictionary', 'FeedBack',
                                       'ReportBug', 'FindFiles', 'ImageViewer', 'InviteFriend', 'Messenger',
                                       'NoteReminder', 'ScreenShot', 'TextEditor', 'PluginManager', 'NodeGraph',
                                       'Browser', ],
                    Extra           = ['ReConfig', 'CleanPyc', 'Debug', 'Snipping Tool'],
                    sysTray         = ['Snipping Tool', 'ScreenShot', 'Maximize', 'Minimize', 'Restore', 'Exit', ], )


    pVERSION = dict(adobe           = ["CC 2017", "CC 2018", "CC 2019", "CC 2020", "CC 2021"],
                    autodesk        = ["2017", "2018", "2019", "2020", "2021"],
                    allegorithmic   = [],
                    foundry         = ["11.1v1", "11.2v1", "4.0v1", "4.1v1", "2.6v3", "4.6v1", "12.0v1", '3.5v2',
                                       '3.2v4', '2.6v3'],
                    pixologic       = ["4R6", "4R7", "4R8", '2018', '2019', '2020', '2021'],
                    sizefx          = ['16.5.439', '16.5.496', '17.5.425', '18.0.327'],
                    office          = ['2017', "2018", "2019", "2020"],
                    jetbrains       = ['2017.3.3', '2018.1', ],
                    wonderUnit      = [],
                    anaconda        = [], )

    pPACKAGE = dict(adobe           = [ "Adobe Photoshop", "Adobe Illustrator", "Adobe Audition", "Adobe After Effects",
                                        "Adobe Premiere Pro", "Adobe Media Encoder", ],
                    autodesk        = [ "Autodesk Maya", "Autodesk Mudbox", "Maya", "Mudbox", "3ds Max", "AutoCAD", ],
                    allegorithmic   = ['Substance Painter', 'Substance Designer'],
                    foundry         = ['Hiero', 'Mari', 'NukeStudio', 'NukeX', 'Katana', ],
                    pixologic       = ['ZBrush'],
                    sizefx          = ['Houdini FX', ],
                    office          = ['Word', 'Excel', 'PowerPoint', 'Wordpad'],
                    jetbrains       = ['JetBrains PyCharm', ],
                    wonderUnit      = ['Storyboarder', 'Krita (x64)', 'Krita (x32)'],
                    anaconda        = ['Spyder', 'QtDesigner', 'Git Bash']
                    )

    windowApps = ['Sublime Text 2', 'Sublime Text 3', 'Wordpad', 'Headus UVLayout',
                  'Snipping Tool', ] + pPACKAGE['anaconda'] + pPACKAGE['office']

    TOOL_UI_KEYS = ['Calculator', 'Calendar', 'EnglishDictionary', 'FindFiles', 'ImageViewer',
                    'NoteReminder', 'ScreenShot', 'TextEditor', ]

    def __init__(self):
        super(TrackKeys, self).__init__()

        self.KEYPACKAGE = self.generate_key_packages()

        self.__dict__.update()

    def generate_key_packages(self, *info):
        keyPackage = []
        for k in self.pPACKAGE:
            for name in self.pPACKAGE[k]:
                if len(self.pVERSION[k]) == 0:
                    key = name
                    keyPackage.append(key)
                else:
                    for ver in self.pVERSION[k]:
                        if name == 'Hiero' or name == 'HieroPlayer' or name == 'NukeX':
                            key = name + " " + ver
                        else:
                            if not ver or ver == []:
                                key = name
                            else:
                                key = name + " " + ver
                        keyPackage.append(key)

        info = keyPackage + self.windowApps

        return info

    def generate_config(self, key):

        info = []

        for k in self.KEYPACKAGE:
            for t in self.pTRACK[key]:
                if t in k:
                    info.append(k)

        return list(sorted(set(info)))

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved