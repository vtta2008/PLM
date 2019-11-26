# -*- coding: utf-8 -*-
"""

Script Name: setup.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
import os, re
from setuptools import setup, find_packages

with open("damg.py", "rb") as f:
    contents = f.read().decode('utf-8')

def parse(pattern):
    return re.search(pattern, contents).group(1).replace('"', '').strip()

def setup_read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), 'r') as f:
        return f.read()

long_description = setup_read('README.md')

version = parse(r'__version__\s+=\s+(.*)')
author = parse(r'__author__\s+=\s+(.*)')
email = parse(r'__email__\s+=\s+(.*)')

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
]

setup(
    name                            = "damg",
    version                         = version,
    author                          = author,
    author_email                    = email,
    description                     = "A package which are damg team style",
    long_description                =  long_description,
    long_description_content_type   = "text/markdown",
    license                         = "MIT",
    zip_safe                        = False,
    py_module                       = ["damg"],
    url                             = "https://github.com/vtta2008/damg",
    packages                        = find_packages(),
    classifiers                     = classifiers,
    install_requires                = ['PyQt5'],
)

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 22/10/2019 - 12:12 AM
# © 2017 - 2018 DAMGteam. All rights reserved