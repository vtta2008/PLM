# -*- coding: utf-8 -*-
"""

Script Name: config.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

import os, json

from damgteam.base import DAMGDICT, DAMG

# -------------------------------------------------------------------------------------------------------------
""" App (python) """

class CONFIG_PATHS(DAMG):

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

    _root                       = os.getenv('ROOT')

    DAMG                        = _root
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

    TAG                         = os.path.join(IMG          , tags)

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

    PLM                         = os.path.join(_root        , assets        , PLM)
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

    SCENEGRAPH                  = os.path.join(_root        , assets        , scenegraph)
    SCENEGRAPH_CFG              = os.path.join(_root        , apps          , config)
    SCENEGRAPH_SETTING          = os.path.join(_root        , apps          , config        , settings)
    SCENEGRAPH_LOG              = os.path.join(_root        , apps          , config        , logs)
    SCENEGRAPH_CACHE            = os.path.join(_root        , apps          , config        , cache)
    SCENEGRAPH_PREF             = os.path.join(_root        , apps          , config        , prefs)

    TOOLKITS                    = os.path.join(_root        , assets        , toolkit)

    NODEGRAPH                   = os.path.join(_root        , assets        , nodegraph)
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

    SETTING_FILEPTH             = dict(app=APP_SETTING, user=USER_SETTING, unix=UNIX_SETTING, format=FORMAT_SETTING)

    def __init__(self):
        DAMG.__init__(self)

        for key, value in self._data.items():
            value = value.replace('\\', '/')
            if not os.path.exists(value):
                os.mkdir(value)

class CONFIG_SETUP(DAMG):

    _oid = 'CFG_SETUP'
    _name = 'configurations for setup.py file'

    _email = "dot@damgteam.com"
    _packages_dir = ["", 'appData', 'bin', 'core', 'imgs', 'plg_ins', 'ui', 'utilities']
    _download = "https://github.com/vtta2008/PipelineTool/releases"
    _description__ = "This applications can be used to build, manage, and optimise film making pipelines."
    _readme = "README.rst"
    _pkgsReq = ['appdirs', 'deprecate', 'msgpack', 'winshell', 'pandas', 'wheel', 'argparse', 'green']
    _modules = []

    __classifiers__ = [

        "Development Status :: 3 - Production/Unstable", "Environment :: X11 Applications :: Qt",
        "Environment :: Win64 (MS Windows)", "Intended Audience :: Freelance Artist :: small VFX studio",
        "License :: OSI Approved :: MIT License", "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.6",

        "Topic :: Software Development :: pipeline-framework :: Application :: vfx :: customization :: optimization :: research-project",]


class CONFIGS(DAMG):

    paths                                       = CONFIG_PATHS()

    def __init__(self):
        DAMG.__init__(self)

        self._data                              = DAMGDICT()
        self.__dict__                           = DAMGDICT()

    _configPths = CONFIG_PATHS()

    @property
    def data(self):

        return self._data




# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 10:56 PM
# Pipeline manager - DAMGteam
