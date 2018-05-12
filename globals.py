#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script Name: globals.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    This script is the place for all global variables

"""
# -------------------------------------------------------------------------------------------------------------
""" Import """
import os, re

__root__ = "PLT_RT"

os.environ[__root__] = os.getcwd()

VERSION = os.path.join(os.getcwd(), 'appData', 'VERSION')
def get_current_version(project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format('__version__'), open(VERSION).read())
    return result.group(1)

__appname__ = "PipelineTool"

__version__ = get_current_version(__appname__)

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
__server__ = "https://pipeline.damgteam.com"

__serverCheck__ = "https://pipeline.damgteam.com/check"

__serverAutho__ = "https://pipeline.damgteam.com/auth"

metadataPth = os.path.join(os.getenv(__root__), 'appData', 'METADATA')
keys = ['__appname__', '__version__', '__packages__', '__pkgsDir__', '__website__', '__download__', '__licence__', '__author__', '__email__',
        '__author__', '__author__', '__description__', '__modules__', '__pkgsReq__', '__classifiers__']

datas = [__appname__, __version__, __packages__, __pkgsDir__, __website__, __download__, __licence__, __author__, __email__,
        __author__, __author__, __description__, __modules__, __pkgsReq__, __classifiers__]

def store_default_metadata():
    f = open(metadataPth, "a+")
    for i in range(len(keys)):
        f.write("{key} = '{data}' \n".format(key=keys[i], data=datas[i]))
    f.close()
    return True

