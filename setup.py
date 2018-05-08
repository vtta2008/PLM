#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Script Name: setup.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    Pipeline Tool installation

"""

import os
import sys
import subprocess

from setuptools import setup

from __init__ import __root__
os.environ[__root__] = os.getcwd()
from __init__ import (__pkgsReq__, __readme__, __appname__, __version__, __licence__, __author__, __modules__, \
    __classifiers__, __description__, __download__, __email__, __packages__, __pkgsDir__, __website__)

for dir in os.listdir(os.getenv(__root__)):
    pltPth = os.path.join(os.getenv(__root__), dir)
    if os.path.isdir(pltPth):
        if not pltPth in sys.path:
            sys.path.append(pltPth)

def install_required_package():
    for pkg in __pkgsReq__:
        try:
            subprocess.Popen("python -m pip install %s" % pkg)
        except FileNotFoundError:
            subprocess.Popen("pip install %s" % pkg)
        finally:
            subprocess.Popen("python -m pip install --upgrade %s" % pkg)

def install_layout_style_package():
    layoutStyle_setupPth = os.path.join(os.getenv(__root__), 'bin', 'qdarkgraystyle', 'setup.py')

    if os.path.exists(layoutStyle_setupPth):
        try:
            import qdarkgraystyle
        except ImportError:
            subprocess.Popen("python setup.py install", cwd=layoutStyle_setupPth)
            return True
        else:
            return False
    else:
        return False

def uninstall_all_required_package():
    for pkg in __pkgsReq__:
        try:
            subprocess.Popen("python -m pip uninstall %s" % pkg)
        except FileNotFoundError:
            subprocess.Popen("pip uninstall %s" % pkg)
            __pkgsReq__.remove(pkg)

    if len(__pkgsReq__)==0:
        return True
    else:
        return False

install_required_package()

layoutStyle_setupPth = os.path.join(os.getenv(__root__), 'bin', 'qdarkgraystyle', 'setup.py')
subprocess.Popen("python setup.py install", cwd=layoutStyle_setupPth.split('setup.py')[0])

with open(__readme__, 'r') as f:
    readme = f.read()

setup(
    name = __appname__,
    version = __version__,
    packages = __packages__,
    package_dir = __pkgsDir__,
    url = __website__,
    download_url = __download__,
    license = __licence__,
    author = __author__,
    author_email=__email__,
    maintainer = __author__,
    maintainer_email = __author__,
    description = __description__,
    long_description = readme,
    py_modules = __modules__,
    install_requires = __pkgsReq__,
    classifiers = __classifiers__,
)
