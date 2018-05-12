#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Script Name: setup.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script will build executable file.

"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
# print("Import from modules: {file}".format(file=__name__))
# print("Directory: {path}".format(path=__file__.split(__name__)[0]))
__root__ = "PLT_RT"
# -------------------------------------------------------------------------------------------------------------
""" Import """
import os
import sys
import globals

from cx_Freeze import setup, Executable

import _version

__appname__ = globals.__appname__

base = None

if sys.platform == "win32":
    base = "Win32GUI"

os.environ[__root__] = os.getcwd()

for dir in os.listdir(os.getenv(__root__)):
    pltPth = os.path.join(os.getenv(__root__), dir)
    if os.path.isdir(pltPth):
        if not pltPth in sys.path:
            sys.path.append(pltPth)

__readme__ = os.path.join(os.getcwd(), 'README.rst')

with open(__readme__, 'r') as f:
    readme = f.read()

includes = ["atexit", "re"]

project = os.getcwd()
__appname__ = "PipelineTool"

__about__ = "About plt"

__organization__ = "DAMG team"

__website__ = "https://pipeline.damgteam.com"

__download__ = "https://github.com/vtta2008/pipelineTool"

__email__ = "dot@damgteam.com"

__author__ = "Trinh Do, Duong Minh Duc"

__description__ = "This applications can be used to build, manage, and optimise film making pipelines."

__readme__ = os.path.join(os.getenv(__root__), 'README.rst')

__licence__ = os.path.join(os.getenv(__root__), 'LICENSE')

__modules__ = ['plt', 'globals', '_version', 'appData.templates.pyTemplate', 'utilities.variables', 'utilities.utils',
               'utilities.sql_server', 'utilities.sql_local', 'utilities.message', 'ui.ui_acc_setting', 'ui.ui_calculator',
               'ui.ui_calendar', 'ui.ui_english_dict', 'ui.ui_find_files', 'ui.ui_image_viewer', 'ui.ui_info_template',
               'ui.ui_new_project', 'ui.ui_note_reminder', 'ui.ui_preference', 'ui.ui_pw_reset_form', 'ui.ui_screenshot', ]
__pkgsReq__ = [ "deprecated", "jupyter-console", "ipywidgets","pywinauto", "winshell", "pandas", "notebook", "juppyter",
                "opencv-python", "pyunpack", "argparse", "qdarkgraystyle", "asyncio", "websockets", "cx_Freeze", ]
__packages__ = ['', 'ui', 'appData', 'utilities']

__pkgsDir__ = { 'bin': os.path.join(os.getenv(__root__), 'bin'),
                'ui': os.path.join(os.getenv(__root__), 'ui'),
                'appData': os.path.join(os.getenv(__root__), 'appData'),
                'utilities': os.path.join(os.getenv(__root__), 'utilities'),}
__classifiers__ = [
              'Development Status :: 3 - Production/Unstable',
              'Environment :: X11 Applications :: Qt',
              'Environment :: Win64 (MS Windows)',
              'Intended Audience :: Artist :: VFX Company',
              'License :: OSI Approved :: MIT License',
              'Operating System :: Microsoft :: Windows',
              'Programming Language :: Python :: 3.6',
              'Topic :: Software Development :: pipeline-framework :: Application :: vfx :: customization :: optimization :: research-project',
                ]

version = _version.get_version(project)

__version__ = version.split("v")[-1].split("dev1")[0] + '1'

setup(
    name = __appname__,
    version = __version__,
    packages =__packages__,
    package_dir = __pkgsDir__,
    url = __website__,
    download_url = __download__,
    license = __licence__,
    author = __author__,
    author_email= __email__,
    maintainer = __author__,
    maintainer_email = __email__,
    description = __description__,
    long_description = readme,
    py_modules = __modules__,
    install_requires =__pkgsReq__,
    classifiers = __classifiers__,
    options = {"build_exe" : {"includes" : includes }},
    executables = [Executable("Plt.py", base = base)],
)
