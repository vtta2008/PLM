# coding=utf-8
"""
Script Name: maya_tk.py
Author: Do Trinh/Jimmy - 3D artist, leader DAMG team.

Description:
    This script will find all the path of modules, icons, images ans store them to a file
"""

import os, sys, json, logging

logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

print os.getenv('PIPELINE_MAYA_TOOLKIT')
