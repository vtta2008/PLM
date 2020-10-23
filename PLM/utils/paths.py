# -*- coding: utf-8 -*-
"""

Script Name: 
Author: Do Trinh/Jimmy - 3D artist.

Description:


"""
# -------------------------------------------------------------------------------------------------------------
import os

from PLM.cores.Errors import DirectoryError

def get_all_path_from_dir(directory):
    """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    filePths = []   # List which will store all of the full file paths.
    dirPths = []    # List which will store all of the full folder paths.

    # Walk the tree.
    for root, directories, files in os.walk(directory, topdown=False):
        for filename in files:
            filePths.append(os.path.join(root, filename).replace('\\', '/'))  # Add to file list.
        for folder in directories:
            dirPths.append(os.path.join(root, folder).replace('\\', '/')) # Add to folder list.
    return [filePths, dirPths]


def get_file_path(directory, filter=None):
    if not os.path.exists(directory):
        return DirectoryError("{0} is not exists.".format(directory))
    else:
        if not filter:
            return get_all_path_from_dir(directory)[0]
        else:
            return [f for f in get_all_path_from_dir(directory)[0] if filter in f]

def get_folder_path(directory):
    if not os.path.exists(directory):
        return DirectoryError("{0} is not exists.".format(directory))
    else:
        return get_all_path_from_dir(directory)[1]

def get_base_folder(path):
    return os.path.dirname(path)

def get_base_name(path):
    return os.path.basename(path)

# -------------------------------------------------------------------------------------------------------------
# Created by Trinh Do on 5/6/2020 - 3:13 AM
# © 2017 - 2020 DAMGteam. All rights reserved