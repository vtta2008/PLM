# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, re
from setuptools                 import find_packages
from cx_Freeze                  import setup, Executable
import PLM
from PLM                        import ROOT
from PLM.configs                import LICENCE, COPYRIGHT

os.environ['TCL_LIBRARY']       = "C:/ProgramData/Anaconda3/tcl/tcl8.6"
os.environ['TK_LIBRARY']        = "C:/ProgramData/Anaconda3/tcl/tk8.6"

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

with open(os.path.join(ROOT, 'configs', 'metadatas.py'), "rb") as f:
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
# install_requires    = __pkgsReq__
classifiers         = parse(r'__classifiers__\s+=\s+(.*)')
keywords            = parse(r'__plmSlogan__\s+=\s+(.*)')

# print(install_requires, type(install_requires))

main_python_file    = "PLM/app.py"

build_exe_options = {'packages': ['os', 'sys', ], "excludes": ["tkinter"]}      #'include_files': includefiles,}
options = {"build_exe" : build_exe_options, 'bdist_msi': {}}


setup(name             = appname,
      version          = PLM.__version__,
      packages         = find_packages(),
      url              = website,
      download_url     = download,
      license          = LICENCE,
      author           = author,
      author_email     = email,
      maintainer       = maintainer,
      maintainer_email = email,
      description      = application_title,
      long_description = readme,
      # install_requires = install_requires,
      classifiers      = classifiers,
      package_data     = {'imgs': [ '{}/*'.format(item) for item in os.listdir('imgs') if os.path.isdir(os.path.join('imgs', item))]},
      keywords         = keywords,
      options          = options,
      zip_safe         = True,
      executables      = [Executable(main_python_file, base=base, copyright=COPYRIGHT,icon = 'logo.ico',), ],
      entry_points     = {"console_scripts": ["my-script = PLM.cli:entry_point"]},
      )

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved
