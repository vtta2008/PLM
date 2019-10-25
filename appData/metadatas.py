# -*- coding: utf-8 -*-
"""

Script Name: metadatas.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals

# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__envKey__              = "DAMGTEAM"

__organization__        = "DAMG TEAM"
__organizationID__      = "DAMG"
__organizationName__    = 'DAMGTEAM'
__groupname__           = "DAMGTEAM"
__softwareName__        = "Pipeline Manager"
__damgSlogan__          = "Comprehensive Solution Design"
__website__             = "https://damgteam.com"
__authors__             = "Trinh Do & Duong Minh Duc"
__author1__             = "Trinh Do"
__author2__             = "Duong Minh Duc"
__Founders__            = __author1__
__CoFonders__           = __author2__
__emails__              = "damgteam@gmail.com"
__email1__              = "dot@damgteam.com"
__email2__              = "up@damgteam.com"

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__             = "PLM"
__appname__             = "Pipeline Manager (PLM)"
__appShortcut__         = "Plm.ink"
__version__             = "13.0.1"
__cfgVersion__          = "0.8.6"
__verType__             = "Dev"
__reverType__           = "2"
__about__               = "About Pipeline Manager"
__homepage__            = "https://pipeline.damgteam.com"
__plmSlogan__           = "Creative your own pipeline"
__plmWiki__             = "https://github.com/vtta2008/PipelineTool/wiki"

# -------------------------------------------------------------------------------------------------------------
""" Server """

__globalServer__        = "https://server.damgteam.com"
__globalServerCheck__         = "https://server.damgteam.com/check"
__globalServerAutho__         = "https://server.damgteam.com/auth"

__localPort__           = "20987"
__localHost__           = "http://localhost:"
__localServer__         = "{0}{1}".format(__localHost__, __localPort__)
__localServerCheck__    = "{0}/check".format(__localServer__)
__localServerAutho__    = "{0}/auth".format(__localServer__)

__google__              = "www.google.com"
__googleVN__            = "www.google.com.vn"
__googleNZ__            = "www.google.co.nz"

# -------------------------------------------------------------------------------------------------------------
""" Metadata """

VERSION                 = "{0} v{1}.{2}-{3}".format(__project__, __version__, __verType__, __reverType__)
COPYRIGHT               = "{0} software (c) 2017-2018 {1}. All rights reserved.".format(__appname__, __organization__)
PLUGINVERSION           = "{0}.13.cfg.{1}".format(__appname__, __cfgVersion__)
PLMAPPID                = "{0}.{1}.{2}.{3}".format(__organization__, __project__, __appname__, VERSION)

API_MAJOR_VERSION       = 0.69
API_REVISION            = 0
API_VERSION             = float('%s%s' % (API_MAJOR_VERSION, API_REVISION))
API_VERSION_AS_STRING   = '%.02f.%d' % (API_MAJOR_VERSION, API_REVISION)
PLATFORM                = 'Windows'
API_MINIMUM             = 0.64

# ----------------------------------------------------------------------------------------------------------- #
""" Setup.py options """

__email__ = __emails__
__packages_dir__ = ["", 'appData', 'bin', 'core', 'imgs', 'plugins', 'scripts', 'ui', 'utils']
__download__ = "https://github.com/vtta2008/PipelineTool/releases"
__description__ = "This applications can be used to build, manage, and optimise film making pipelines."
__readme__ = "README.rst"
__pkgsReq__ = ['PyQt5', 'pip', 'urllib3', 'chardet', 'appdirs', 'deprecate', 'msgpack', 'winshell',
               'pyqtwebengine', 'pandas', 'wheel', 'argparse', 'green']
__modules__ = []
__classifiers__ = [

    "Development Status :: 3 - Production/Unstable", "Environment :: X11 Applications :: Qt",
    "Environment :: Win64 (MS Windows)", "Intended Audience :: Freelance Artist :: small VFX studio",
    "License :: OSI Approved :: MIT License", "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: pipeline-framework :: Application :: vfx :: customization :: optimization :: research-project",

                    ]

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 13/05/2019 - 9:50 AM
# © 2017 - 2018 DAMGteam. All rights reserved