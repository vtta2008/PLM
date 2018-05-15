#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: __init__.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
print("Import from modules: {file}".format(file=__name__))
print("Directory: {path}".format(path=__file__.split(__name__)[0]))

# -------------------------------------------------------------------------------------------------------------
""" Import """

__envKey__ = "PIPELINE_TOOL"

__project__ = "Pipeline Tool"

__version__ = "13.0.1"

__appname__ = "PipelineTool"

__about__ = "About plt"

__organization__ = "DAMG team"

__website__ = "https://pipeline.damgteam.com"

__download__ = "https://github.com/vtta2008/pipelineTool"

__email__ = "dot@damgteam.com, up@damgteam.com"

__author__ = "Trinh Do, Duong Minh Duc"

__description__ = "This applications can be used to build, manage, and optimise film making pipelines."

__readme__ = "README.rst"

__modules__ = ["plt", "globals", "_version", "appData.templates.pyTemplate", "utilities.variables", "utilities.utils",
               "utilities.sql_server", "utilities.sql_local", "utilities.message", "ui.ui_acc_setting", "ui.ui_calculator",
               "ui.ui_calendar", "ui.ui_english_dict", "ui.ui_find_files", "ui.ui_image_viewer", "ui.ui_info_template",
               "ui.ui_new_project", "ui.ui_note_reminder", "ui.ui_preference", "ui.ui_pw_reset_form", "ui.ui_screenshot", ]
__pkgsReq__ = [ "deprecated", "jupyter-console", "ipywidgets","pywinauto", "winshell", "pandas", "notebook", "juppyter",
                "opencv-python", "pyunpack", "argparse", "qdarkgraystyle", "asyncio", "websockets", "cx_Freeze", ]

__packages_dir__ = ["", "ui", "appData", "appPackages", "docs", "imgs", "utilities"]


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

__server__ = "https://pipeline.damgteam.com"

__serverCheck__ = "https://pipeline.damgteam.com/check"

__serverAutho__ = "https://pipeline.damgteam.com/auth"

VERSION = "{0} v{1}".format(__project__, __version__)