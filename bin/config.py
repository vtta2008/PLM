# -*- coding: utf-8 -*-
"""

Script Name: config.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

import re, os, json

# Python
from PyQt5.QtCore import Qt, QSettings, QDateTime, QSize
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsView, QGraphicsScene, QSizePolicy, QRubberBand, QFrame
from PyQt5.QtGui import QPainter, QColor

try:
    from importlib import reload
except ImportError:
    pass

PLMAPPID = "Pipeline Manager v13.0.0"

from appData import __envKey__

about                       = "about"                    # A
app                         = 'app'
apps                        = 'apps'
assets                      = '_assets'
authors                     = "authors"
avatar                      = "avatar"

bin                         = 'bin'                      # B
build                       = 'build'

cache                       = 'cache'                    # C
config                      = '.config'
core                        = 'core'

DAMGteam                    = 'DAMGteam'                 # D
data                        = 'data'
dependencies                = 'dependencies'
dock                        = 'dock'
docs                        = 'docs'

ico                         = 'ico'                      # I
icons                       = 'icons'
imgs                        = 'imgs'
installation                = 'installation'

LICENSE                     = 'LICENSE'                  # L
logo                        = 'logo'
logo32                      = 'logo32'
logs                        = 'logs'

maya                        = 'maya'                     # M

name                        = "name"                     # N
nodegraph                   = 'nodegraph'

pics                        = 'pics'                     # P
Plm                         = 'Plm'
PLM                         = 'PLM'
PLM_TANK                    = 'PLM_TANK'
plugins                     = 'plugins'
prefs                       = 'prefs'
product                     = "product"

qss                         = 'qss'                      # Q

reg                         = 'reg'                      # R
resources                   = 'resources'

scenegraph                  = 'SceneGraph'               # S
scripts                     = 'scripts'
settings                    = 'settings'
shortcut                    = "shortcut"
slogan                      = "slogan"
state                       = "state"
status                      = "status"

t                           = 't'                        # T
tags                        = 'tags'
toolkit                     = 'toolkit'

userPrefs                   = 'userPrefs'                # U

web                         = 'web'                      # W
website                     = "website"
wiki                        = "wiki"

x16                         = "x16"                      # x
x24                         = "x24"
x32                         = "x32"
x48                         = "x48"
x64                         = "x64"
x128                        = "x128"

# ----------------------------------------------------------------------------------------------------------- #
""" Path """

_root                       = os.getenv(__envKey__)

DAMG_CFG                    = os.path.join(_root        , app           , config)
DAMG_SETTING                = os.path.join(DAMG_CFG     , settings)
DAMG_LOG                    = os.path.join(DAMG_CFG     , logs)
DAMG_CACHE                  = os.path.join(DAMG_CFG     , cache)
DAMG_PREF                   = os.path.join(DAMG_CFG     , prefs)

BIN                         = os.path.join(_root        , bin)

BINDATA                     = os.path.join(BIN          , data)
BINDATA_JSON                = os.path.join(BINDATA      , 'json')
BINDATA_DOC                 = os.path.join(BINDATA      , docs)

DEPENDANCIES                = os.path.join(BIN          , dependencies)

BINRESCR                    = os.path.join(BIN          , resources)
BINRESCR_DOC                = os.path.join(BINRESCR     , docs)
LICENCE                     = os.path.join(BINRESCR_DOC , LICENSE)

SCRIPTS                     = os.path.join(BINDATA      , scripts)

TYPES                       = os.path.join(BINDATA      , 'types')

IMG                         = os.path.join(BINRESCR     , imgs)

AVATAR                      = os.path.join(IMG          , avatar)

ICON                        = os.path.join(IMG          , icons)
ICON_16                     = os.path.join(ICON         , x16)
ICON_24                     = os.path.join(ICON         , x24)
ICON_32                     = os.path.join(ICON         , x32)
ICON_48                     = os.path.join(ICON         , x48)
ICON_64                     = os.path.join(ICON         , x64)

LOGO                        = os.path.join(IMG          , logo)

DAMG_LOGO                   = os.path.join(LOGO         , DAMGteam)
DAMG_ICO                    = os.path.join(DAMG_LOGO    , ico)
DAMG_ICON                   = os.path.join(DAMG_LOGO    , icons)
DAMG_ICON_32                = os.path.join(DAMG_ICON    , logo32)

PLM_LOGO                    = os.path.join(LOGO         , Plm)
PLM_ICO                     = os.path.join(PLM_LOGO     , ico)
PLM_ICON                    = os.path.join(PLM_LOGO     , icons)
PLM_ICON_32                 = os.path.join(PLM_ICON     , logo32)

MAYA_ICON                   = os.path.join(IMG          , maya)

PIC                         = os.path.join(IMG          , pics)

TAG_ICON                    = os.path.join(IMG          , tags)

WEB_ICON                    = os.path.join(IMG          , web)
WEB_ICON_16                 = os.path.join(WEB_ICON     , x16)
WEB_ICON_24                 = os.path.join(WEB_ICON     , x24)
WEB_ICON_32                 = os.path.join(WEB_ICON     , x32)
WEB_ICON_48                 = os.path.join(WEB_ICON     , x48)
WEB_ICON_64                 = os.path.join(WEB_ICON     , x64)
WEB_ICON_128                = os.path.join(WEB_ICON     , x128)

INSTALLATION                = os.path.join(BINRESCR     , installation)

QSS                         = os.path.join(BINRESCR     , qss)

BUILD                       = os.path.join(_root        , build)

CORE                        = os.path.join(_root        , core)

DOCK                        = os.path.join(_root        , dock)

PLUGINS                     = os.path.join(_root        , plugins)

TEST                        = os.path.join(_root        , t)

ASSETS                      = os.path.join(_root        , assets)
ASSETS_CFG                  = os.path.join(_root        , apps)

PLM_ROOT                    = os.path.join(_root        , assets        , PLM)
PLM_CFG                     = os.path.join(_root        , apps          , config)
PLM_SETTING                 = os.path.join(_root        , apps          , config        , settings)
PLM_LOG                     = os.path.join(_root        , apps          , config        , logs)
PLM_CACHE                   = os.path.join(_root        , apps          , config        , cache)
PLM_PREF                    = os.path.join(_root        , apps          , config        , prefs)

PLM_TANK                    = os.path.join(_root        , assets        , PLM_TANK)
PLM_TANK_CFG                = os.path.join(_root        , apps          , config)
PLM_TANK_SETTING            = os.path.join(_root        , apps          , config        , settings)
PLM_TANK_LOG                = os.path.join(_root        , apps          , config        , logs)
PLM_TANK_CACHE              = os.path.join(_root        , apps          , config        , cache)
PLM_TANK_PREF               = os.path.join(_root        , apps          , config        , prefs)

SCENEGRAPH_ROOT             = os.path.join(_root        , assets        , scenegraph)
SCENEGRAPH_CFG              = os.path.join(_root        , apps          , config)
SCENEGRAPH_SETTING          = os.path.join(_root        , apps          , config        , settings)
SCENEGRAPH_LOG              = os.path.join(_root        , apps          , config        , logs)
SCENEGRAPH_CACHE            = os.path.join(_root        , apps          , config        , cache)
SCENEGRAPH_PREF             = os.path.join(_root        , apps          , config        , prefs)

TOOLKITS                    = os.path.join(_root        , assets        , toolkit)

NODEGRAPH_ROOT              = os.path.join(_root        , assets        , nodegraph)
NODEGRAPH_CFG               = os.path.join(_root        , apps          , config)
NODEGRAPH_SETTING           = os.path.join(_root        , apps          , config        , settings)
NODEGRAPH_LOG               = os.path.join(_root        , apps          , config        , logs)
NODEGRAPH_CACHE             = os.path.join(_root        , apps          , config        , cache)
NODEGRAPH_PREF              = os.path.join(_root        , apps          , config        , prefs)

iconcfg                     = os.path.join(PLM_CFG      , 'icons.cfg')                  # Config app icon path
webIconCfg                  = os.path.join(PLM_CFG      , 'webIcon.cfg')                # Config Web icon path
logoIconCfg                 = os.path.join(PLM_CFG      , 'logoIcon.cfg')               # Config logo icon path

pyEnvCfg                    = os.path.join(PLM_CFG      , 'envKey.cfg')                 # Config python env variables
appConfig                   = os.path.join(PLM_CFG      , 'main.cfg')                   # Config pipeline soft package
mainConfig                  = os.path.join(PLM_CFG      , 'PLM.cfg')                    # Master config

APP_SETTING                 = os.path.join(PLM_SETTING  , 'PLM.ini')                    # Pipeline application setting
USER_SETTING                = os.path.join(PLM_SETTING  , 'user.ini')                   # User setting
FORMAT_SETTING              = os.path.join(PLM_SETTING  , 'format.ini')
UNIX_SETTING                = os.path.join(PLM_SETTING  , 'unix.ini')

DB_PTH                      = os.path.join(BINDATA      , 'local.db')                   # Local database
LOG_PTH                     = os.path.join(PLM_LOG      , 'PLM.logs')                   # Log file

PROGRAM64                   = os.getenv('PROGRAMFILES')
PROGRAM86                   = os.getenv('PROGRAMFILES(X86)')
LOCALAPPDATA                = os.getenv('APPDATA')
PROGRAMDATA                 = os.getenv('PROGRAMDATA')

SETTING_FILEPTH             = dict(app=APP_SETTING, user=USER_SETTING, unix=UNIX_SETTING, format=FORMAT_SETTING)

# ----------------------------------------------------------------------------------------------------------- #
""" Setup.py options """

__email__               = "dot@damgteam.com"
__packages_dir__        = ["", 'appData', 'bin', 'core', 'imgs', 'plg_ins', 'ui', 'utilities']
__download__            = "https://github.com/vtta2008/PipelineTool/releases"
__description__         = "This applications can be used to build, manage, and optimise film making pipelines."
__readme__              = "README.rst"
__pkgsReq__             = ['appdirs', 'deprecate', 'msgpack', 'winshell', 'pandas', 'wheel', 'argparse', 'green']
__modules__             = []
__classifiers__         = [

    "Development Status :: 3 - Production/Unstable" , "Environment :: X11 Applications :: Qt"                       ,
    "Environment :: Win64 (MS Windows)"             , "Intended Audience :: Freelance Artist :: small VFX studio"   ,
    "License :: OSI Approved :: MIT License"        , "Operating System :: Microsoft :: Windows"                    ,
    "Programming Language :: Python :: 3.6"         ,

    "Topic :: Software Development :: pipeline-framework :: Application :: vfx :: customization :: optimization :: research-project",
                    ]

def reload_module(module):
    return reload(module)

def read_file(fileName):
    filePth = os.path.join(os.getenv(__envKey__), 'bin', 'resources', 'docs', fileName + '.txt')

    with open(filePth, 'r') as f:
        data = f.read()
    return data

QUESTIONS           = read_file('QUESTION')
ABOUT               = read_file('ABOUT')
CREDIT              = read_file('CREDIT')
CODECONDUCT         = read_file('CODECONDUCT')
CONTRIBUTING        = read_file('CONTRIBUTING')
REFERENCE           = read_file('REFERENCE')
LICENCE_MIT         = read_file('LICENCE/MIT')
LICENCE_APACHE      = read_file('LICENCE/APACHE')

# --------------------------------------------------------------------------------------------------------------
""" Autodesk config """

autodeskVer         = [ "2017", "2018", "2019", "2020"]
autodeskApp         = [ "Autodesk Maya", "Autodesk MudBox", "Autodesk 3ds Max", "Autodesk AutoCAD"]
userMayaDir         = os.path.expanduser(r"~/Documents/maya")

# --------------------------------------------------------------------------------------------------------------
""" Adobe config """

adobeVer            = [ "CC 2017", "CC 2018", "CC 2019", ]
adobeApp            = [ "Adobe Photoshop", "Adobe Illustrator", "Adobe Audition", "Adobe After Effects", "Adobe Premiere Pro",
                        "Adobe Media Encoder", ]

# --------------------------------------------------------------------------------------------------------------
""" Foundry config """

foundryVer          = [ "11.1v1", "11.2v1", "4.0v1", "4.1v1", "2.6v3"]
foundryApp          = [ 'Hiero', 'HieroPlayer', 'Mari', 'NukeX', 'Katana',]

# --------------------------------------------------------------------------------------------------------------
""" Pixologic config """

pixologiVer         = [ "4R6", "4R7", "4R8"]
pixologiApp         = [ 'ZBrush', ]

# --------------------------------------------------------------------------------------------------------------
""" Allegorithmic config """

allegorithmicVer    = [ ]

allegorithmicApp    = [ 'Substance Painter', 'Substance Designer']

# --------------------------------------------------------------------------------------------------------------
""" SideFX config """

sizefxVer           = [ '16.5.439', '16.5.496']
sizefxApp           = [ 'Houdini FX', ]

# --------------------------------------------------------------------------------------------------------------
""" Microsoft Office config """

officeVer           = [ '2013', '2015', '2016', '2017' ]
officeApp           = [ 'Word', 'Excel', 'PowerPoint', 'Wordpad', 'TextEditor', 'NoteReminder' ]

# --------------------------------------------------------------------------------------------------------------
""" JetBrains config """

jetbrainsVer        = [ '2017.3.3', '2018.1', ]
jetbrainsApp        = [ 'JetBrains PyCharm', ]

# --------------------------------------------------------------------------------------------------------------
""" Wonder Unit """

wonderUnitVer       = [ ]
wonderUniApp        = [ 'Storyboarder', 'Krita (x64)' ]

# --------------------------------------------------------------------------------------------------------------
""" another app config """

anacondaApp         = [ 'Spyder', 'QtDesigner', 'Git Bash']
otherApp            = [ 'Sublime Text 2', 'Sublime Text 3', 'Wordpad', 'Headus UVLayout', 'Snipping Tool', ]
CONFIG_APPUI        = [ 'About', 'Calculator', 'Calendar', 'Credit', 'EnglishDictionary', 'FindFiles', 'ForgotPassword',
                        'ImageViewer', 'NewProject', 'Preferences', 'Screenshot', 'UserSetting', 'PLMBrowser', 'NoteReminder',
                        'TextEditor', 'NodeGraph']

# --------------------------------------------------------------------------------------------------------------
""" Tracking configKey """

TRACK_TDS           = [ 'Maya', 'ZBrush', 'Houdini', '3Ds Max', 'Mudbox', 'BLender', ]
TRACK_VFX           = [ 'NukeX', 'After Effects', 'katana']
TRACK_ART           = [ 'Photoshop', 'Illustrator', 'Storyboarder', 'Krita (x64)']
TRACK_TEX           = [ 'Mari', 'Painter', ]
TRACK_POST          = [ 'Davinci Resolve', 'Hiero', 'HieroPlayer', 'Premiere Pro']
TRACK_OFFICE        = [ 'Word', 'Excel', 'PowerPoint', 'Wordpad']
TRACK_DEV           = [ 'PyCharm', 'Sublime Text', 'QtDesigner', 'Git Bash', 'Command Prompt', 'Spyder']
TRACK_TOOLS         = [ 'Calculator', 'Calendar', 'EnglishDictionary', 'FindFiles', 'ImageViewer', 'Screenshot', 'NodeGraph']
TRACK_EXTRA         = [  ]
TRACK_SYSTRAY       = [ 'Snipping Tool', 'Screenshot', 'Maximize', 'Minimize', 'Restore', 'Quit', ]
KEYDETECT           = [ "Non-commercial", "Uninstall", "Verbose", "License", "Skype", ".url"]
FIX_KEY             = { 'Screenshot': 'screenShot', 'Snipping Tool': 'SnippingTool'}

# --------------------------------------------------------------------------------------------------------------
""" Combine config data """

pVERSION = dict(adobe=adobeVer, autodesk=autodeskVer, allegorithmic = allegorithmicVer, foundry=foundryVer,
                pixologic=pixologiVer, sizefx=sizefxVer, office=officeVer, jetbrains=jetbrainsVer, wonderUnit=wonderUnitVer, )

pPACKAGE = dict(adobe=adobeApp, autodesk=autodeskApp, allegorithmic = allegorithmicApp, foundry=foundryApp,
                pixologic=pixologiApp, sizefx=sizefxApp, office=officeApp, jetbrains=jetbrainsApp, wonderUnit=wonderUniApp,)

pTRACK = dict(TDS=TRACK_TDS, VFX=TRACK_VFX, ART=TRACK_ART, TEXTURE = TRACK_TEX, POST = TRACK_POST,
              Office=TRACK_OFFICE, Dev=TRACK_DEV, Tools=TRACK_TOOLS, Extra=TRACK_EXTRA, sysTray=TRACK_SYSTRAY, )

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
CONFIG_TDS      = generate_config('TDS')                            # TD artist
CONFIG_VFX      = generate_config('VFX')                            # VFX artist
CONFIG_ART      = generate_config('ART')                            # 2D artist
CONFIG_TEX      = generate_config('TEXTURE')                        # ShadingTD artist
CONFIG_POST     = generate_config('POST')                           # Post production

# Tab 1 sections config
CONFIG_OFFICE   = generate_config('Office')                         # Paper work department
CONFIG_DEV      = generate_config('Dev') + ['Command Prompt']       # Rnd - Research and development
CONFIG_TOOLS    = generate_config('Tools')                          # useful/custom tool supporting for the whole pipeline
CONFIG_EXTRA    = generate_config('Extra')                          # Extra tool may be considering to use
CONFIG_SYSTRAY  = generate_config('sysTray')

# -------------------------------------------------------------------------------------------------------------
""" Format """

ST_FORMAT = dict(   ini       = QSettings.IniFormat,
                    native    = QSettings.NativeFormat,
                    invalid   = QSettings.InvalidFormat, )

datetTimeStamp = QDateTime.currentDateTime().toString("hh:mm - dd MMMM yy")             # datestamp

IMGEXT = "All Files (*);;Img Files (*.jpg);;Img Files (*.png)"

# -------------------------------------------------------------------------------------------------------------
""" Nodegraph setting variables """

ASPEC_RATIO                 = Qt.KeepAspectRatio

SCROLLBAROFF                = Qt.ScrollBarAlwaysOff                                     # Scrollbar
SCROLLBARON                 = Qt.ScrollBarAlwaysOn
SCROLLBARNEED               = Qt.ScrollBarAsNeeded

# -------------------------------------------------------------------------------------------------------------
""" UI flags """

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
NOANCHOR                    = QGraphicsView.NoAnchor

ANCHOR_UNDERMICE            = QGraphicsView.AnchorUnderMouse
ANCHOR_VIEWCENTER           = QGraphicsView.AnchorViewCenter

CACHE_BG                    = QGraphicsView.CacheBackground

UPDATE_VIEWRECT             = QGraphicsView.BoundingRectViewportUpdate
UPDATE_FULLVIEW             = QGraphicsView.FullViewportUpdate
UPDATE_SMARTVIEW            = QGraphicsView.SmartViewportUpdate
UPDATE_BOUNDINGVIEW         = QGraphicsView.BoundingRectViewportUpdate
UPDATE_MINIMALVIEW          = QGraphicsView.MinimalViewportUpdate

# -------------------------------------------------------------------------------------------------------------
""" Drawing """

ANTIALIAS                   = QPainter.Antialiasing                                     # Painter
ANTIALIAS_TEXT              = QPainter.TextAntialiasing
ANTIALIAS_HIGH_QUALITY      = QPainter.HighQualityAntialiasing
SMOOTH_PIXMAP_TRANSFORM     = QPainter.SmoothPixmapTransform
NON_COSMETIC_PEN            = QPainter.NonCosmeticDefaultPen

BRUSH_NONE                  = Qt.NoBrush                                                # Brush

PEN_NONE                    = Qt.NoPen                                                  # Pen
ROUND_CAP                   = Qt.RoundCap
ROUND_JOIN                  = Qt.RoundJoin

PATTERN_SOLID               = Qt.SolidPattern                                           # Pattern

LINE_SOLID                  = Qt.SolidLine                                              # Line

COLOR_LIBS = dict(

    WHITE                   = Qt.white,                                                  # Color
    LIGHTGRAY               = Qt.lightGray,
    GRAY                    = Qt.gray,
    DARKGRAY                = Qt.darkGray,
    BLACK                   = Qt.black,
    RED                     = Qt.red,
    GREEN                   = Qt.green,
    BLUE                    = Qt.blue,
    DARKRED                 = Qt.darkGreen,
    DARKGREEN               = Qt.darkGreen,
    DARKBLUE                = Qt.darkBlue,
    CYAN                    = Qt.cyan,
    MAGENTA                 = Qt.magenta,
    YELLOW                  = Qt.yellow,
    DARKCYAN                = Qt.darkCyan,
    DARKMAGENTA             = Qt.darkMagenta,
    DARKYELLOW              = Qt.darkYellow,

    blush                   = QColor(246, 202, 203, 255),
    petal                   = QColor(247, 170, 189, 255),
    petunia                 = QColor(231, 62, 151, 255),
    deep_pink               = QColor(229, 2, 120, 255),
    melon                   = QColor(241, 118, 110, 255),
    pomegranate             = QColor(178, 27, 32, 255),
    poppy_red               = QColor(236, 51, 39, 255),
    orange_red              = QColor(240, 101, 53, 255),
    olive                   = QColor(174, 188, 43, 255),
    spring                  = QColor(227, 229, 121, 255),
    yellow                  = QColor(255, 240, 29, 255),
    mango                   = QColor(254, 209, 26, 255),
    cantaloupe              = QColor(250, 176, 98, 255),
    tangelo                 = QColor(247, 151, 47, 255),
    burnt_orange            = QColor(236, 137, 36, 255),
    bright_orange           = QColor(242, 124, 53, 255),
    moss                    = QColor(176, 186, 39, 255),
    sage                    = QColor(212, 219, 145, 255),
    apple                   = QColor(178, 215, 140, 255),
    grass                   = QColor(111, 178, 68, 255),
    forest                  = QColor(69, 149, 62, 255),
    peacock                 = QColor(21, 140, 167, 255),
    teal                    = QColor(24, 157, 193, 255),
    aqua                    = QColor(153, 214, 218, 255),
    violet                  = QColor(55, 52, 144, 255),
    deep_blue               = QColor(15, 86, 163, 255),
    hydrangea               = QColor(150, 191, 229, 255),
    sky                     = QColor(139, 210, 244, 255),
    dusk                    = QColor(16, 102, 162, 255),
    midnight                = QColor(14, 90, 131, 255),
    seaside                 = QColor(87, 154, 188, 255),
    poolside                = QColor(137, 203, 225, 255),
    eggplant                = QColor(86, 5, 79, 255),
    lilac                   = QColor(222, 192, 219, 255),
    chocolate               = QColor(87, 43, 3, 255),
    blackout                = QColor(19, 17, 15, 255),
    stone                   = QColor(125, 127, 130, 255),
    gravel                  = QColor(181, 182, 185, 255),
    pebble                  = QColor(217, 212, 206, 255),
    sand                    = QColor(185, 172, 151, 255),
  )

# -------------------------------------------------------------------------------------------------------------
""" Keyboard and cursor """

KEYBOARD                    = Qt.Key                                                    # Keyboard
KEY_ALT                     = Qt.Key_Alt
KEY_DEL                     = Qt.Key_Delete
KEY_TAB                     = Qt.Key_Tab
KEY_SHIFT                   = Qt.Key_Shift
KEY_CTRL                    = Qt.Key_Control
KEY_BACKSPACE               = Qt.Key_Backspace
KEY_F                       = Qt.Key_F
KEY_S                       = Qt.Key_S
ALT_MODIFIER                = Qt.AltModifier
CTRL_MODIFIER               = Qt.ControlModifier
SHIFT_MODIFIER              = Qt.ShiftModifier
NO_MODIFIER                 = Qt.NoModifier
CLOSE_HAND_CUSOR            = Qt.ClosedHandCursor

windows                     = os.name = 'nt'
DMK                         = Qt.AltModifier if windows else CTRL_MODIFIER

MOUSE_LEFT                  = Qt.LeftButton
MOUSE_RIGHT                 = Qt.RightButton
MOUSE_MIDDLE                = Qt.MiddleButton

ARROW_NONE                  = Qt.NoArrow                                                # Cursor
CURSOR_ARROW                = Qt.ArrowCursor
CURSOR_SIZEALL              = Qt.SizeAllCursor

ACTION_MOVE                 = Qt.MoveAction                                             # Action

# -------------------------------------------------------------------------------------------------------------
""" Set number """

RELATIVE_SIZE               = Qt.RelativeSize                                           # Size

POSX                        = 0
POSY                        = 0

NODE_WIDTH                  = 200
NODE_ROUND                  = 10
NODE_BORDER                 = 2
NODE_REC                    = 30
NODE_STAMP                  = 25

NODE_HEADER_HEIGHT          = 25
NODE_FOOTER_HEIGHT          = 25

ATTR_HEIGHT                 = 30
ATTR_ROUND                  = NODE_ROUND/2
ATTR_REC                    = NODE_REC/2

RADIUS                      = 10
COL                         = 10
ROW                         = 10
GRID_SIZE                   = 50

FLTR                        = 'flow_left_to_right'
FRTL                        = 'flow_right_to_left'

MARGIN                      = 20
ROUNDNESS                   = 0
THICKNESS                   = 1
CURRENT_ZOOM                = 1

UNIT                        = 60                                                                # Base Unit
MARG                        = 5                                                                 # Content margin
BUFF                        = 10                                                                # Buffer size
SCAL                        = 1                                                                 # Scale value
STEP                        = 1                                                                 # Step value changing
VAL                         = 1                                                                 # Default value
MIN                         = 0                                                                 # Minimum value
MAX                         = 1000                                                              # Maximum value
WMIN                        = 50                                                                # Minimum width
HMIN                        = 20                                                                # Minimum height
HFIX                        = 80
ICONSIZE                    = 32
ICONBUFFER                  = -1
BTNICONSIZE                 = QSize(ICONSIZE, ICONSIZE)
ICONBTNSIZE                 = QSize(ICONSIZE+ICONBUFFER, ICONSIZE+ICONBUFFER)

keepARM                     = Qt.KeepAspectRatio
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
hori                        = Qt.Horizontal
vert                        = Qt.Vertical

dockL                       = Qt.LeftDockWidgetArea                                             # Docking area
dockR                       = Qt.RightDockWidgetArea
dockT                       = Qt.TopDockWidgetArea
dockB                       = Qt.BottomDockWidgetArea

# -------------------------------------------------------------------------------------------------------------
""" Node graph pre setting """

# node connection property types
PROPERTY = dict( simple = ['FLOAT', 'STRING', 'BOOL', 'INT'] , arrays  = ['FLOAT2', 'FLOAT3', 'INT2', 'INT3', 'COLOR'],
                 max    = 'maximum value'                    , types   = ['FILE', 'MULTI', 'MERGE', 'NODE', 'DIR']    ,
                 min    = 'minimum value'                    , default = 'default value'                              ,
                 label  = 'node label'                       , private = 'attribute is private (hiddent)'             ,
                 desc   = 'attribute description',)

REGEX   = dict( section        = re.compile(r"^\[[^\]\r\n]+]"),
                section_value  = re.compile(r"\[(?P<attr>[\w]*?) (?P<value>[\w\s]*?)\]$"),
                properties     = re.compile("(?P<name>[\.\w]*)\s*(?P<type>\w*)\s*(?P<value>.*)$"),)

# Default preferences
PREFERENCES = dict(
    ignore_scene_prefs  = {"default": False,     "desc": "Use user prefences instead of scene preferences.", "label": "Ignore scene preferences",    "class": "global"},
    use_gl              = {"default": False,     "desc": "Render graph with OpenGL.",                        "label": "Use OpenGL",                  "class": "scene" },
    edge_type           = {"default": "bezier",  "desc": "Draw edges with bezier paths.",                    "label": "Edge name",                  "class": "scene" },
    render_fx           = {"default": False,     "desc": "Render node drop shadows and effects.",            "label": "render FX",                   "class": "scene" },
    antialiasing        = {"default": 2,         "desc": "Antialiasing level.",                              "label": "Antialiasing",                "class": "scene" },
    logging_level       = {"default": 30,        "desc": "Verbosity level.",                                 "label": "Logging level",               "class": "global"},
    autosave_inc        = {"default": 90000,     "desc": "Autosave delay (seconds x 1000).",                 "label": "Autosave time",               "class": "global"},
    stylesheet_name     = {"default": "default", "desc": "Stylesheet to use.",                               "label": "Stylesheet",                  "class": "global"},
    palette_style       = {"default": "default", "desc": "Color palette to use.",                            "label": "Palette",                     "class": "global"},
    font_style          = {"default": "default", "desc": "font name to use.",                               "label": "Font name",                  "class": "global"},
    viewport_mode       = {"default": "smart",   "desc": "viewport update fn.",                              "label": "Viewport Mode",               "class": "global"}, )

VALID_FONTS = dict( ui   = [ 'Arial', 'Cantarell', 'Corbel', 'DejaVu Sans', 'DejaVu Serif', 'FreeSans', 'Liberation Sans',
                             'Lucida Sans Unicode', 'MS Sans Serif', 'Open Sans', 'PT Sans', 'Tahoma', 'Verdana'],

                    mono = [ 'Consolas', 'Courier', 'Courier 10 Pitch', 'Courier New', 'DejaVu Sans Mono', 'Fixed',
                             'FreeMono', 'Liberation Mono', 'Lucida Console', 'Menlo', 'Monaco'],

                    nodes= [ 'Consolas', 'DejaVu Sans Mono', 'Menlo', 'DejaVu Sans'])

EDGE_TYPES      = dict(bezier = 'bezier'        , polygon = 'polygon'       , )
POS_EVENTS      = dict(change = POS_CHANGE      , )
DRAG_MODES      = dict(none   = NODRAG          , rubber = RUBBER_DRAG)
VIEWPORT_MODES  = dict(full   = UPDATE_FULLVIEW , smart  = UPDATE_SMARTVIEW , minimal = UPDATE_MINIMALVIEW  , bounding = UPDATE_BOUNDINGVIEW, viewrect = UPDATE_VIEWRECT)
FLAG_MODES      = dict(select = SELECTABLE      , move   = MOVEABLE         , focus   = FOCUSABLE           , panel    = PANEL)
ANCHOR_MODES    = dict(none   = NOANCHOR        , under  = ANCHOR_UNDERMICE , center  = ANCHOR_VIEWCENTER   , )


NODE            = dict( width               = NODE_WIDTH            , height       = 25              , radius                 = 10                  , border    = 2 ,
                        attHeight           = 30                    , con_width    = 2               , font                   = 'Arial'             , font_size = 12,
                        attFont             = 'Arial'               , attFont_size = 10              , mouse_bounding_box     = 80                  , alternate= 20,
                        grid_color          = [50, 50, 50, 255]     , slot_border  = [50, 50, 50, 255], non_connectable_color = [100, 100, 100, 255],
                        connection_color    = [255, 155, 0, 255], )

SCENE           = dict( width               = 2000                  , height = 2000                 , size              = 36       , antialiasing = True,
                        antialiasing_boost  = True                  , smooth_pixmap = True, )

# -------------------------------------------------------------------------------------------------------------
""" PLM project base """

PRJ_INFO = dict( APPS               = ["maya", "zbrush", "mari", "nuke", "photoshop", "houdini", "after effects"],
                 MASTER             = ["_assets", "sequences", "deliverables", "documents", "editorial", "sound", "resources", "RnD"],
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

FIX_KEYS = dict( TextEditor         = 'textEditor', NoteReminder = 'noteReminder',  Calculator  = 'calculator',  Calendar  = 'calendar',
                 EnglishDictionary  = 'engDict',    FindFiles    = 'findFile',      ImageViewer = 'imageViewer', NodeGraph = 'nodeGraph',
                 Screenshot         = 'screenShot', )

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 31/08/2018 - 6:46 PM
# © 2017 - 2018 DAMGteam. All rights reserved