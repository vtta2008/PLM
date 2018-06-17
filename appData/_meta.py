# -*- coding: utf-8 -*-
"""

Script Name: _meta.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" DAMG team """

__organization__ = "DAMG team"
__damgSlogan__ = "Comprehensive Solution Design"
__website__ = "https://damgteam.com"
__author1__ = "Trinh Do"
__author2__ = "Duong Minh Duc"
__Founder__ = __author1__
__CoFonder1__ = __author2__
__email1__ = "dot@damgteam.com"
__email2__ = "up@damgteam.com"

# -------------------------------------------------------------------------------------------------------------
""" PipelineTool """

__project__ = "Pipeline Manager (Plm)"
__appname__ = "PLM"
__appShortcut__ = "Plm.ink"
__version__ = "13.0.1"
__cfgVersion__ = "0.8.6"
__verType__ = "Dev"
__reverType__ = "2"
__about__ = "About Pipeline Manager"
__homepage__ = "https://pipeline.damgteam.com"
__plmSlogan__ = "Creative your own pipeline"
__plmWiki__ = "https://github.com/vtta2008/PipelineTool/wiki"

# -------------------------------------------------------------------------------------------------------------
""" Server """

__serverLocal__ = "http://127.0.0.1:8000/"
__serverUrl__ = "https://pipeline.damgteam.com"
__serverCheck__ = "https://pipeline.damgteam.com/check"
__serverAutho__ = "https://pipeline.damgteam.com/auth"

__google__ = "https://google.com.vn"

# -------------------------------------------------------------------------------------------------------------
""" Metadata """

VERSION = "{0} v{1}.{2}-{3}".format(__project__, __version__, __verType__, __reverType__)
COPYRIGHT = "{0} software (c) 2017-2018 {1}. All rights reserved.".format(__appname__, __organization__)
PLUGINVERSION = "{0}.13.cfg.{1}".format(__appname__, __cfgVersion__)
PLMAPPID = u'{0}.{1}.{2}.{3}'.format(__organization__, __project__, __appname__, VERSION)

API_MAJOR_VERSION = 0.69
API_REVISION = 0
API_VERSION = float('%s%s' % (API_MAJOR_VERSION, API_REVISION))
API_VERSION_AS_STRING = '%.02f.%d' % (API_MAJOR_VERSION, API_REVISION)
PLATFORM = 'Windows'
API_MINIMUM = 0.64

# ----------------------------------------------------------------------------------------------------------- #
""" Setup.py options """

__email__ = __email1__ + ", " + __email2__

__packages_dir__ = ["", "ui", "appData", "tankers", "docs", "imgs", "utilities"]

__classifiers__ = [
              "Development Status :: 3 - Production/Unstable",
              "Environment :: X11 Applications :: Qt",
              "Environment :: Win64 (MS Windows)",
              "Intended Audience :: Artist :: VFX Company",
              "License :: OSI Approved :: MIT License",
              "Operating System :: Microsoft :: Windows",
              "Programming Language :: Python :: 3.6",
              "Topic :: Software Development :: pipeline-framework :: Application :: vfx :: customization :: optimization :: research-project",
                ]

__download__ = "https://github.com/vtta2008/PipelineTool/releases"

__description__ = "This applications can be used to build, manage, and optimise film making pipelines."

__readme__ = "README.rst"

__modules__ = ["plm", "globals", "_version", "appData.templates.pyTemplate", "utilities.variables", "utilities.utils",
               "utilities.sql_server", "utilities.sql_local", "utilities.message", "ui.ui_acc_setting", "ui.ui_calculator",
               "ui.ui_calendar", "ui.ui_english_dict", "ui.ui_find_files", "ui.ui_image_viewer", "ui.ui_info_template",
               "ui.ui_new_project", "ui.ui_note_reminder", "ui.ui_preference", "ui.ui_pw_reset_form", "ui.ui_screenshot", ]

__pkgsReq__ = [ "deprecated", "jupyter-console", "ipywidgets","pywinauto", "winshell", "pandas", "notebook", "juppyter",
                "opencv-python", "pyunpack", "argparse", "qdarkgraystyle", "asyncio", "websockets", "cx_Freeze", ]

# ----------------------------------------------------------------------------------------------------------- #
# Created by panda on 3/06/2018 - 11:36 PM
# Pipeline manager - DAMGteam
