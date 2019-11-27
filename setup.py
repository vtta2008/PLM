# -*- coding: utf-8 -*-
"""

Script Name: setup.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    This script will build executable file.

"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import

""" Setup envronment configKey to be able to work """

import re
from setuptools import find_packages

# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
from cx_Freeze import setup, Executable

# PLM
from __buildtins__ import *

from appData import LICENCE_MIT, APP_DATA_DIR, COPYRIGHT, __pkgsReq__

from cores.Version import version

os.environ['TCL_LIBRARY']   = "C:/ProgramData/Anaconda3/tcl/tcl8.6"
os.environ['TK_LIBRARY']    = "C:/ProgramData/Anaconda3/tcl/tk8.6"

if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = None

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your qssPths files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)

with open(os.path.join(APP_DATA_DIR, 'metadatas.py'), "rb") as f:
    metadata = f.read().decode('utf-8')

def parse(pattern):
    return re.search(pattern, metadata).group(1).replace('"', '').strip()

with open('README.rst', 'r') as f:
    readme = f.read()

appname             = parse(r'__appname__\s+=\s+(.*)')
packages            = parse(r'__packages_dir__\s+=\s+(.*)')
application_title   = parse(r'__project__\s+=\s+(.*)')
website             = parse(r'__website__\s+=\s+(.*)')
download            = parse(r'__download__\s+=\s+(.*)')
author              = parse(r'__author__\s+=\s+(.*)')
maintainer          = parse(r'__author1__\s+=\s+(.*)')
maintainer_email    = parse(r'__email__\s+=\s+(.*)')
email               = parse(r'__email__\s+=\s+(.*)')
install_requires    = __pkgsReq__
classifiers         = parse(r'__classifiers__\s+=\s+(.*)')
keywords            = parse(r'__plmSlogan__\s+=\s+(.*)')

print(install_requires, type(install_requires))

main_python_file    = "main.py"

build_exe_options = {'packages': ['os', 'sys', ], "excludes": ["tkinter"]}      #'include_files': includefiles,}
options = {"build_exe" : build_exe_options, 'bdist_msi': {}}


setup(name             = appname,
      version          = version(),
      packages         = find_packages(),
      url              = website,
      download_url     = download,
      license          = LICENCE_MIT,
      author           = author,
      author_email     = email,
      maintainer       = maintainer,
      maintainer_email = email,
      description      = application_title,
      long_description = readme,
      install_requires = install_requires,
      classifiers      = classifiers,
      package_data     = {'imgs': [ '{}/*'.format(item) for item in os.listdir('imgs') if os.path.isdir(os.path.join('imgs', item))]},
      keywords         = keywords,
      options          = options,
      zip_safe         = True,
      executables      = [Executable(main_python_file, base=base, copyright=COPYRIGHT,icon = 'logo.ico',), ]
      )

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 19/06/2018 - 2:26 AM
# © 2017 - 2018 DAMGteam. All rights reserved