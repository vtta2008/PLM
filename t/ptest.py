# -*- coding: utf-8 -*-
"""

Script Name: ptest.py
Author: Do Trinh/Jimmy - 3D artist.

Description:

"""
# -------------------------------------------------------------------------------------------------------------
# import subprocess
# import pkg_resources
#
# def update_python_packages():
#     pkgs = [(d.project_name, d.version) for d in pkg_resources.working_set]
#
#     for p in pkgs:
#         pkg = p[0]
#         print('upgrade python package: {0}'.format(pkg))
#         subprocess.Popen("python -m pip install {0} --user -- upgrade".format(pkg), shell=True).wait()
#         print('finished upgrade: {0}'.format(pkg))
#
#     print('all finished')
#
#
# from core.DRegistry import ClassRegistry, ClassRegistryInstanceCache
#
# pokedex = ClassRegistry('element')
#
# @pokedex.register
# class Pikachu(object):
#   element = 'electric'
#
# @pokedex.register
# class Alakazam(object):
#   element = 'psychic'
#
# print(type(pokedex))

# import os, stat
#
# def get_all_path_from_dir(directory):
#     """
#         This function will generate the file names in a directory
#         tree by walking the tree either top-down or bottom-up. For each
#         directory in the tree rooted at directory top (including top itself),
#         it yields a 3-tuple (dirpath, dirnames, filenames).
#     """
#     filePths = []   # List which will store all of the full file paths.
#     dirPths = []    # List which will store all of the full folder paths.
#
#     # Walk the tree.
#     for root, directories, files in os.walk(directory, topdown=False):
#         for filename in files:
#             filePths.append(os.path.join(root, filename))  # Add to file list.
#         for folder in directories:
#             dirPths.append(os.path.join(root, folder)) # Add to folder list.
#     return [filePths, dirPths]
#
# def get_file_path(directory):
#     return get_all_path_from_dir(directory)[0]
#
# def get_folder_path(directory):
#     return get_all_path_from_dir(directory)[1]
#
# dir = r"G:/New folder/set"
#
# files = [f for f in get_file_path(dir) if f.endswith('.pdf')]
#
# for f in files:
#     print(os.stat(f))

import os, pprint

for k in os.environ.keys():
    print(k)

print(os.getenv('PROGRAMFILES'))
print(os.getenv('PROGRAMFILES(X86)'))

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 18/08/2018 - 8:42 PM
# © 2017 - 2018 DAMGteam. All rights reserved