# -*- coding: utf-8 -*-
'''

Script Name: path.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

'''
# -------------------------------------------------------------------------------------------------------------

# Python
import os

# PLM
from .winConfigs                            import ConfigPcs
from .baseConfigs                           import Pys, Urls, Lgs, Fnts, Dirs, Pths, Ics, Apps, Fmts, Uis, Clrs, Pls, Cmds

from PLM                                    import glbSettings, create_path, ROOT
from PLM.types                              import CMD_VALUE_TYPE
from PLM.api.Core                           import Size, DateTime
from PLM.api.Gui                            import Painter, Font

# PyQt5
from PyQt5.QtCore                           import Qt, QEvent

from PyQt5.QtWidgets                        import (QGraphicsItem, QGraphicsView, QGraphicsScene, QRubberBand, QFrame,
                                                    QSizePolicy, QLineEdit, QPlainTextEdit, QAbstractItemView, QStyle, )


SYS_OPTS                                    = ["Host Name", "OS Name", "OS Version", "Product ID", "System Manufacturer",
                                                "System Model", "System type", "BIOS Version", "Domain", "Windows Directory",
                                                "Total Physical Memory", "Available Physical Memory", "Logon Server"]



notKeys                                      = ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__',
                                                '__cached__', '__builtins__', 'os', '__envKey__', 'cfgdir', 'CFG_DIR',
                                                'SETTING_DIR', 'DB_DIR', 'LOG_DIR', 'QSS_DIR', 'RCS_DIR', 'SCSS_DIR',
                                                '__appname__', 'subprocess', 'unicode_literals', 'absolute_import',
                                                '__organization__']


IGNORE_ICONS                                = [ 'Widget', 'bright', 'dark', 'charcoal', 'nuker', 'TopTab1', 'TopTab2',
                                                'Organisation', 'Project', 'Team', 'Task', 'ShowAll','ItemWidget',
                                                'BaseManager', 'SettingInput', 'QueryPage', 'SysTray', 'Footer', 'BotTab1',
                                                'BotTab2', 'Cmd', 'User', 'Tracking']


datetTimeStamp                              = DateTime.currentDateTime().toString("hh:mm - dd MMMM yy")             # datestamp



# -------------------------------------------------------------------------------------------------------------
""" Event """

NO_WRAP                     = QPlainTextEdit.NoWrap
NO_FRAME                    = QPlainTextEdit.NoFrame
ELIDE_RIGHT                 = Qt.ElideRight
ELIDE_NONE                  = Qt.ElideNone


# -------------------------------------------------------------------------------------------------------------
""" Window state """

StateNormal                 = Qt.WindowNoState
StateMax                    = Qt.WindowMaximized
StateMin                    = Qt.WindowMinimized
State_Selected              = QStyle.State_Selected

# -------------------------------------------------------------------------------------------------------------
""" Nodegraph setting variables """

ASPEC_RATIO                 = Qt.KeepAspectRatio
SMOOTH_TRANS                = Qt.SmoothTransformation
SCROLLBAROFF                = Qt.ScrollBarAlwaysOff                                     # Scrollbar
SCROLLBARON                 = Qt.ScrollBarAlwaysOn
SCROLLBARNEED               = Qt.ScrollBarAsNeeded

WORD_WRAP                   = Qt.TextWordWrap
INTERSECT_ITEM_SHAPE        = Qt.IntersectsItemShape
CONTAIN_ITEM_SHAPE          = Qt.ContainsItemShape
MATCH_EXACTLY               = Qt.MatchExactly
DRAG_ONLY                   = QAbstractItemView.DragOnly

# -------------------------------------------------------------------------------------------------------------
""" UI flags """

ITEMENABLE                  = Qt.ItemIsEnabled
ITEMMOVEABLE                = QGraphicsItem.ItemIsMovable
ITEMSENDGEOCHANGE           = QGraphicsItem.ItemSendsGeometryChanges
ITEMSCALECHANGE             = QGraphicsItem.ItemScaleChange
ITEMPOSCHANGE               = QGraphicsItem.ItemPositionChange
DEVICECACHE                 = QGraphicsItem.DeviceCoordinateCache
SELECTABLE                  = QGraphicsItem.ItemIsSelectable
MOVEABLE                    = QGraphicsItem.ItemIsMovable
FOCUSABLE                   = QGraphicsItem.ItemIsFocusable
PANEL                       = QGraphicsItem.ItemIsPanel

NOINDEX                     = QGraphicsScene.NoIndex                                    # Scene

RUBBER_DRAG                 = QGraphicsView.RubberBandDrag                              # Viewer
RUBBER_REC                  = QRubberBand.Rectangle
POS_CHANGE                  = QGraphicsItem.ItemPositionChange

NODRAG                      = QGraphicsView.NoDrag
NOFRAME                     = QGraphicsView.NoFrame
ANCHOR_NO                   = QGraphicsView.NoAnchor

ANCHOR_UNDERMICE            = QGraphicsView.AnchorUnderMouse
ANCHOR_CENTER               = QGraphicsView.AnchorViewCenter

CACHE_BG                    = QGraphicsView.CacheBackground

UPDATE_VIEWRECT             = QGraphicsView.BoundingRectViewportUpdate
UPDATE_FULLVIEW             = QGraphicsView.FullViewportUpdate
UPDATE_SMARTVIEW            = QGraphicsView.SmartViewportUpdate
UPDATE_BOUNDINGVIEW         = QGraphicsView.BoundingRectViewportUpdate
UPDATE_MINIMALVIEW          = QGraphicsView.MinimalViewportUpdate

STAY_ON_TOP                 = Qt.WindowStaysOnTopHint
STRONG_FOCUS                = Qt.StrongFocus
SPLASHSCREEN                = Qt.SplashScreen
FRAMELESS                   = Qt.FramelessWindowHint
CUSTOMIZE                   = Qt.CustomizeWindowHint
CLOSEBTN                    = Qt.WindowCloseButtonHint
MINIMIZEBTN                 = Qt.WindowMinimizeButtonHint
AUTO_COLOR                  = Qt.AutoColor

# -------------------------------------------------------------------------------------------------------------
""" Drawing """

ANTIALIAS                   = Painter.Antialiasing                                     # Painter
ANTIALIAS_TEXT              = Painter.TextAntialiasing
ANTIALIAS_HIGH_QUALITY      = Painter.HighQualityAntialiasing
SMOOTH_PIXMAP_TRANSFORM     = Painter.SmoothPixmapTransform
NON_COSMETIC_PEN            = Painter.NonCosmeticDefaultPen

NO_BRUSH                    = Qt.NoBrush                                                # Brush

NO_PEN                      = Qt.NoPen                                                  # Pen
ROUND_CAP                   = Qt.RoundCap
ROUND_JOIN                  = Qt.RoundJoin

PATTERN_SOLID               = Qt.SolidPattern                                           # Pattern

LINE_SOLID                  = Qt.SolidLine                                              # Line
LINE_DASH                   = Qt.DashLine
LINE_DOT                    = Qt.DotLine
LINE_DASH_DOT               = Qt.DashDotDotLine

TRANSPARENT                 = Qt.transparent
TRANSPARENT_MODE            = Qt.TransparentMode

# -------------------------------------------------------------------------------------------------------------
""" Meta Object """

QUEUEDCONNECTION            = Qt.QueuedConnection


# -------------------------------------------------------------------------------------------------------------
""" Keyboard and cursor """

TEXT_BOLD                   = Font.Bold
TEXT_NORMAL                 = Font.Normal
MONO_SPACE                  = Font.Monospace

TEXT_MENEOMIC               = Qt.TextShowMnemonic


KEY_PRESS                   = QEvent.KeyPress
KEY_RELEASE                 = QEvent.KeyRelease
KEY_ALT                     = Qt.Key_Alt
KEY_DEL                     = Qt.Key_Delete
KEY_TAB                     = Qt.Key_Tab
KEY_SHIFT                   = Qt.Key_Shift
KEY_CTRL                    = Qt.Key_Control
KEY_BACKSPACE               = Qt.Key_Backspace
KEY_ENTER                   = Qt.Key_Enter
KEY_RETURN                  = Qt.Key_Return
KEY_F                       = Qt.Key_F
KEY_S                       = Qt.Key_S
ALT_MODIFIER                = Qt.AltModifier
CTRL_MODIFIER               = Qt.ControlModifier
SHIFT_MODIFIER              = Qt.ShiftModifier
NO_MODIFIER                 = Qt.NoModifier
CLOSE_HAND_CUSOR            = Qt.ClosedHandCursor
SIZEF_CURSOR                = Qt.SizeFDiagCursor

windows                     = os.name = 'nt'
DMK                         = Qt.AltModifier if windows else CTRL_MODIFIER

MOUSE_LEFT                  = Qt.LeftButton
MOUSE_RIGHT                 = Qt.RightButton
MOUSE_MIDDLE                = Qt.MiddleButton
NO_BUTTON                   = Qt.NoButton

ARROW_NONE                  = Qt.NoArrow                                                # Cursor
CURSOR_ARROW                = Qt.ArrowCursor
CURSOR_SIZEALL              = Qt.SizeAllCursor

ACTION_MOVE                 = Qt.MoveAction                                             # Action

# -------------------------------------------------------------------------------------------------------------
""" Set number """

RELATIVE_SIZE               = Qt.RelativeSize                                           # Size


ICONSIZE                    = 32
ICONBUFFER                  = -1
BTNTAGSIZE                  = Size(87, 20)
TAGBTNSIZE                  = Size(87-1, 20-1)
BTNICONSIZE                 = Size(ICONSIZE, ICONSIZE)
ICONBTNSIZE                 = Size(ICONSIZE+ICONBUFFER, ICONSIZE+ICONBUFFER)

ignoreARM                   = Qt.IgnoreAspectRatio

scrollAsNeed                = Qt.ScrollBarAsNeeded
scrollOff                   = Qt.ScrollBarAlwaysOff
scrollOn                    = Qt.ScrollBarAlwaysOn

SiPoMin                     = QSizePolicy.Minimum                                               # Size policy
SiPoMax                     = QSizePolicy.Maximum
SiPoExp                     = QSizePolicy.Expanding
SiPoPre                     = QSizePolicy.Preferred
SiPoIgn                     = QSizePolicy.Ignored

frameStyle                  = QFrame.Sunken | QFrame.Panel

center                      = Qt.AlignCenter                                                    # Alignment
right                       = Qt.AlignRight
left                        = Qt.AlignLeft
top                         = Qt.AlignTop
bottom                      = Qt.AlignBottom
hori                        = Qt.Horizontal
vert                        = Qt.Vertical

dockL                       = Qt.LeftDockWidgetArea                                             # Docking area
dockR                       = Qt.RightDockWidgetArea
dockT                       = Qt.TopDockWidgetArea
dockB                       = Qt.BottomDockWidgetArea
dockAll                     = Qt.AllDockWidgetAreas


# -------------------------------------------------------------------------------------------------------------
""" setting """

PRS =       dict(password    = QLineEdit.Password,       center = center ,   left  = left   ,    right  = right,
                 spmax       = SiPoMax           ,       sppre  = SiPoPre,   spexp = SiPoExp,    spign  = SiPoIgn,
                 expanding   = QSizePolicy.Expanding,    spmin  = SiPoMin,)

""" PLM project base """

PRJ_INFO = dict( APPS               = ["maya", "zbrush", "mari", "nuke", "photoshop", "houdini", "after effects"],
                 MASTER             = ["assets", "sequences", "deliverables", "docs", "editorial", "sound", "rcs", "RnD"],
                 TASKS              = ["art", "plt_model", "rigging", "surfacing"],
                 SEQTASKS           = ["anim", "comp", "fx", "layout", "lighting"],
                 ASSETS             = {"heroObj": ["washer", "dryer"], "environment": [], "props": []},
                 STEPS              = ["publish", "review", "work"],
                 MODELING           = ["scenes", "fromZ", "toZ", "objImport", "objExport", "movie"],
                 RIGGING            = ["scenes", "reference"],
                 SURFACING          = ["scenes", "sourceimages", "images", "movie"],
                 LAYOUT             = ["scenes", "sourceimages", "images", "movie", "alembic"],
                 LIGHTING           = ["scenes", "sourceimages", "images", "cache", "reference"],
                 FX                 = ["scenes", "sourceimages", "images", "cache", "reference", "alembic"],
                 ANIM               = ["scenes", "sourceimages", "images", "movie", "alembic"],)

FIX_KEYS = dict( TextEditor         = 'TextEditor', NoteReminder = 'NoteReminder',  Calculator  = 'Calculator',
                 Calendar           = 'Calendar', EnglishDictionary  = 'EnglishDictionary',    FindFiles    = 'FindFiles',
                 ImageViewer        = 'ImageViewer', NodeGraph = 'NodeGraph', Screenshot = 'Screenshot', )




# -------------------------------------------------------------------------------------------------------------
""" Config qssPths from text file """


def read_file(fileName):

    filePth = create_path(ROOT, 'docs', 'raws', fileName)

    if os.path.exists(filePth):
        with open(filePth) as f:
            data = f.read()
        return data
    else:
        print("File not found: {0}".format(filePth))



ABOUT                               = read_file('ABOUT')
CODEOFCONDUCT                       = read_file('CODEOFCONDUCT')
CONTRIBUTING                        = read_file('CONTRIBUTING')
COPYRIGHT                           = read_file('COPYRIGHT')
CREDIT                              = read_file('CREDIT')
LICENCE                             = read_file('LICENSE')
LINKS                               = read_file('LINKS')
REFERENCES                          = read_file('REFERENCES')
QUESTIONS                           = read_file('QUESTION')
VERSION                             = read_file('VERSION')

class ConfigColors(Clrs):

    key                             = 'ConfigColors'

    def __init__(self):
        super(ConfigColors, self).__init__()

        self.__dict__.update()

        if glbSettings.printCfgInfo:
            if glbSettings.printColorInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveColorInfo:
                self.save_data()


class ConfigDirs(Dirs):


    key                             = 'ConfigDirs'


    def __init__(self):
        super(ConfigDirs, self).__init__()

        self.__dict__.update()

        if glbSettings.printCfgInfo:
            if glbSettings.printDirInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveDirInfo:
                self.save_data()



class ConfigPths(Pths):

    key                             = 'ConfigPths'

    def __init__(self):
        super(ConfigPths, self).__init__()

        self.__dict__.update()

        if glbSettings.printCfgInfo:
            if glbSettings.printPthInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.savePthInfo:
                self.save_data()



class ConfigIcons(Ics):

    key                                 = 'ConfigIcons'

    def __init__(self):
        super(ConfigIcons, self).__init__()

        if glbSettings.printCfgInfo:
            if glbSettings.printIconInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveIconInfo:
                self.save_data()



class ConfigApps(Apps):

    key                         = 'ConfigApps'

    def __init__(self):
        super(ConfigApps, self).__init__()

        if glbSettings.printCfgInfo:
            if glbSettings.printAppInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveAppInfo:
                self.save_data()



class ConfigPython(Pys):

    key                         = 'ConfigPython'

    def __init__(self):
        super(ConfigPython, self).__init__()


        if glbSettings.printCfgInfo:
            if glbSettings.printPythonInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.savePythonInfo:
                self.save_data()



class ConfigUrls(Urls):

    key                             = 'ConfigUrls'

    def __init__(self):
        super(ConfigUrls, self).__init__()

        if glbSettings.printCfgInfo:
            if glbSettings.printUrlInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveUrlInfo:
                self.save_data()



class ConfigLogos(Lgs):

    key                                 = 'ConfigLogos'

    def __init__(self):
        super(ConfigLogos, self).__init__()

        if glbSettings.printCfgInfo:
            if glbSettings.printAvatarInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveAvatarInfo:
                self.save_data()



class ConfigFonts(Fnts):

    key                                 = 'ConfigFonts'

    def __init__(self):
        super(ConfigFonts, self).__init__()

        if glbSettings.printCfgInfo:
            if glbSettings.printFontInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveFontInfo:
                self.save_data()


class ConfigFormats(Fmts):

    key                                 = 'ConfigFormats'

    def __iter__(self):
        super(ConfigFormats, self).__iter__()

        if glbSettings.printCfgInfo:
            if glbSettings.printFmtInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveFmtInfo:
                self.save_data()


class ConfigUiKeys(Uis):

    key                                 = 'ConfigUiKeys'

    def __iter__(self):
        super(ConfigUiKeys, self).__iter__()

        self.__dict__.update()

        if glbSettings.printCfgInfo:
            if glbSettings.printUiKeyInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.saveUiKeyInfo:
                self.save_data()


iconMissing                     = []
toolTips                        = {}
statusTips                      = {}


class ConfigPipeline(Pls):

    key                         = 'ConfigPipeline'

    dirInfo                     = ConfigDirs()
    pthInfo                     = ConfigPths()
    iconInfo                    = ConfigIcons()
    appInfo                     = ConfigApps()
    urlInfo                     = ConfigUrls()
    uiKeyInfo                   = ConfigUiKeys()


    def __init__(self):
        super(ConfigPipeline, self).__init__()

        removeKeys              = []
        launchAppKeys           = []

        KEYDETECT               = self.uiKeyInfo.KEYDETECT
        KEYPACKAGE              = self.uiKeyInfo.KEYPACKAGE
        OPEN_URL_KEYS           = self.uiKeyInfo.OPEN_URL_KEYS
        SYS_CMD_KEYS            = self.uiKeyInfo.SYS_CMD_KEYS
        OPEN_DIR_KEYS           = self.uiKeyInfo.OPEN_DIR_KEYS
        APP_EVENT_KEYS          = self.uiKeyInfo.APP_EVENT_KEYS
        STYLESHEET_KEYS         = self.uiKeyInfo.STYLESHEET_KEYS
        SHORTCUT_KEYS           = self.uiKeyInfo.SHORTCUT_KEYS

        functionKeys            = self.uiKeyInfo.APP_FUNCS_KEYS
        layoutKeys              = self.uiKeyInfo.APP_UI_KEYS


        for key in self.appInfo:
            if 'NukeX' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --nukex"
            elif 'Hiero' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --hiero"
            elif 'UVLayout' in key:
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " -launch"

        for key in KEYDETECT:
            for k in self.appInfo:
                if key in k:
                    removeKeys.append(k)

        for k in removeKeys:
            self.del_key(k)

        self.appInfo.update()

        for k in KEYPACKAGE:
            for key in self.appInfo.keys():
                if k in key:
                    launchAppKeys.append(key)

        qtDesigner = create_path(os.getenv('PROGRAMDATA'), 'Anaconda3', 'Library', 'bin', 'designer.exe')
        davinciPth = create_path(os.getenv('PROGRAMFILES'), 'Blackmagic Design', 'DaVinci Resolve', 'resolve.exe')

        eVal       = [qtDesigner, davinciPth]
        eKeys      = ['QtDesigner', 'Davinci Resolve']

        for i in range(len(eVal)):
            if os.path.exists(eVal[i]):
                self.appInfo[eKeys[i]] = eVal[i]
                launchAppKeys.append(eKeys[i])

        for key in launchAppKeys:
            try:
                icon = self.iconInfo['icon32'][key]
            except KeyError:
                icon = key
                iconMissing.append(key)
            finally:
                toolTips[key] = 'Launch {0}'.format(key)
                statusTips[key] = 'Launch {0}: {1}'.format(key, self.appInfo[key])
                value = self.appInfo[key]
                valueType = CMD_VALUE_TYPE['pth']
                arg = value
                if 'NukeX' in key:
                    code = 'os.system'
                elif 'Hiero' in key:
                    code = 'os.system'
                elif 'UVLayout' in key:
                    code = 'os.system'
                else:
                    code = 'os.startfile'

            tooltip = toolTips[key]
            statustip = statusTips[key]
            self.add(key, Cmds(key, icon, tooltip, statustip, value, valueType, arg, code))

        for key in functionKeys:

            try:
                icon = self.iconInfo['tag'][key]
            except KeyError:
                try:
                    icon = self.iconInfo['icon32'][key]
                except KeyError:
                    icon = key
                    iconMissing.append(key)
            finally:
                if key in OPEN_URL_KEYS:
                    toolTips[key] = 'Go to {0} website'.format(key)
                    statusTips[key] = 'Open URL: {0}'.format(self.urlInfo[key])
                    value = self.urlInfo[key]
                    valueType = CMD_VALUE_TYPE['url']
                    arg = value
                    code = 'openURL'
                elif key in SYS_CMD_KEYS:
                    toolTips[key] = 'Open command prompt'
                    statusTips[key] = 'Open command prompt'
                    value = 'start /wait cmd'
                    valueType = CMD_VALUE_TYPE['cmd']
                    arg = value
                    code = 'os.system'
                elif key in OPEN_DIR_KEYS:
                    toolTips[key] = 'Open {0} folder'.format(key.replace('Folder', ''))
                    statusTips[key] = 'Open {0} folder'.format(key.replace('Folder', ''))
                    value = self.dirInfo[key]
                    valueType = CMD_VALUE_TYPE['dir']
                    arg = value
                    code = 'os.startfile'
                elif key in APP_EVENT_KEYS:
                    toolTips[key] = 'Release PLM Event: {0}'.format(key)
                    statusTips[key] = 'Activate Event: {0}'.format(key)
                    value = key
                    valueType = CMD_VALUE_TYPE['event']
                    arg = key
                    code = 'appEvent'
                elif key in STYLESHEET_KEYS:
                    toolTips[key] = 'Load stylesheet: {0}'.format(key)
                    statusTips[key] = 'Load stylesheet: {0}'.format(key)
                    value = key
                    valueType = CMD_VALUE_TYPE['stylesheet']
                    arg = value
                    code = 'stylesheet'
                elif key in SHORTCUT_KEYS:
                    toolTips[key] = key
                    statusTips[key] = key
                    value = key
                    valueType = CMD_VALUE_TYPE['shortcut']
                    arg = value
                    code = 'shortcut'
                else:
                    toolTips[key] = 'Execute function: {0}'.format(key)
                    statusTips[key] = 'Execute function: {0}'.format(key)
                    value = key
                    valueType = CMD_VALUE_TYPE['func']
                    arg = value
                    code = 'function'

            tooltip = toolTips[key]
            statustip = statusTips[key]
            self.add(key, Cmds(key, icon, tooltip, statustip, value, valueType, arg, code))

        for key in layoutKeys:
            if not key in launchAppKeys:
                # print(key)
                try:
                    icon = self.iconInfo['icon32'][key]
                except KeyError:
                    icon = key
                    iconMissing.append(key)
                finally:
                    toolTips[key] = 'Show: {0}'.format(key)
                    statusTips[key] = 'Show: {0}'.format(key)
                    value = key
                    valueType = CMD_VALUE_TYPE['uiKey']
                    arg = value
                    code = 'showUI'

                tooltip = toolTips[key]
                statustip = statusTips[key]
                self.add(key, Cmds(key, icon, tooltip, statustip, value, valueType, arg, code))

        if glbSettings.printCfgInfo:
            if glbSettings.printPlmInfo:
                self.pprint()

        if glbSettings.saveCfgInfo:
            if glbSettings.savePlmInfo:
                self.save_data()

    def del_key(self, key):
        try:
            del self.appInfo[key]
        except KeyError:
            self.appInfo.pop(key, None)


# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:45 PM
# Pipeline manager - DAMGteam
