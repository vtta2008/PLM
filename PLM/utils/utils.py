#!/usr/bin/env python3
# coding=utf-8
"""
Script Name: utils.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    Here is where a lot of function need to use multiple times overall
"""
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, winshell, yaml, json, re, linecache

from PIL                import Image
from resizeimage        import resizeimage

# PyQt5
from PyQt5.QtCore       import pyqtSignal, pyqtSlot

# PLM
from PLM                import __envKey__
from PLM.commons.Core   import EventLoop, Timer


# -------------------------------------------------------------------------------------------------------------
""" Destop tool """

def wait(msec):
    loop = EventLoop()
    Timer.singleShot(msec, loop.quit())
    loop.exec_()

def create_shotcut(target, icon, shortcut, description):
    winshell.CreateShortcut(
        Path=os.path.join(winshell.desktop(), shortcut),
        Target=target,
        Icon=(icon, 0),
        Description=description
    )

def create_folder(pth, mode=0o770):
    if not pth or os.path.exists(pth):
        return []

    (head, tail) = os.path.split(pth)
    res = create_folder(head, mode)
    try:
        original_umask = os.umask(0)
        os.makedirs(pth, mode)
    except:
        os.chmod(pth, mode)
    finally:
        os.umask(original_umask)
    res += [pth]
    return res

def create_signal(argType=None, name=None):

    if not name or name is None:
        if argType is None:
            return pyqtSignal()
        else:
            return pyqtSignal(argType)
    else:
        if argType is None:
            return pyqtSignal(name=name)
        else:
            return pyqtSignal(argType, name=name)

def create_slot(argType=None, name=None):

    if not name or name is None:
        if argType is None:
            return pyqtSlot()
        else:
            return pyqtSlot(argType)
    else:
        if argType is None:
            return pyqtSlot(name=name)
        else:
            return pyqtSlot(argType, name=name)

def create_signal_slot(argType, name):
    signal = create_signal(argType, name)
    slot   = create_slot(argType, name)
    return signal, slot



# -------------------------------------------------------------------------------------------------------------
""" Error handle """

def handle_path_error(directory=None):
    if not os.path.exists(directory) or directory is None:
        try:
            raise ("IsADirectoryError: Path is not exists: {directory}".format(directory=directory))
        except IsADirectoryError as error:
            raise('Caught error: ' + repr(error))

def raise_exception():

    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)

    print("--------------------------------------------------------------------------------- \n"
            "Tracking from:   {0} \n"
            "At line number:  {1} \n"
            "Details code:    {2} \n"
            "{3} \n"
            "---------------------------------------------------------------------------------".format(os.path.basename(filename), lineno, line.strip(), exc_obj))
    return


# -------------------------------------------------------------------------------------------------------------
""" Find Path """

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

def get_file_path(directory):
    handle_path_error(directory)
    return get_all_path_from_dir(directory)[0]

def get_folder_path(directory):
    handle_path_error(directory)
    return get_all_path_from_dir(directory)[1]

def get_base_folder(path):
    return os.path.dirname(path)

def get_base_name(path):
    return os.path.basename(path)

def generate_alternative_color(color, av):
    lightness = color.lightness()
    mult = float(lightness)/255
    return mult



# -------------------------------------------------------------------------------------------------------------
""" Read, Write, Edit json/yaml/_data info """

def data_handler(type='json', mode='r', filePath=None, data={}):

    if type == 'json':
        if mode == 'r' or mode == 'r+':
            with open(filePath, mode) as f:
                info = json.load(f)
        elif mode == 'w' or mode == 'w+':
            with open(filePath, mode) as f:
                info = json.dump(data, f, indent=4)
        else:
            with open(filePath, mode) as f:
                info = json.dump(data, f, indent=4)
    else:
        if mode == 'r' or mode == 'r+':
            with open(filePath, mode) as f:
                info = yaml.load(f)
        elif mode == 'w' or mode == 'w+':
            with open(filePath, mode) as f:
                info = yaml.dump(data, f, default_flow_style=False)
        else:
            with open(filePath, mode) as f:
                info = yaml.dump(data, f, default_flow_style=False)
    return info

def swap_list_index(inputList, oldIndex, newIndex):
    if oldIndex == -1:
        oldIndex = len(inputList)-1
    if newIndex == -1:
        newIndex = len(inputList)
    value = inputList[oldIndex]
    inputList.pop(oldIndex)
    inputList.insert(newIndex, value)

def load_config(filePath):
    with open(filePath, 'r') as myfile:
        fileString = myfile.read()
        cleanString = re.sub('//.*?\n|/\*.*?\*/', '', fileString, re.S)                 # remove comments
        data = json.loads(cleanString)
    return data

def save_data(filePath, data):
    f = open(filePath, "w")
    f.write(json.dumps(data, sort_keys = True, indent = 4, ensure_ascii=False))
    f.close()

def load_data(filePath):
    with open(filePath) as json_file:
        j_data = json.load(json_file)
    json_file.close()
    return j_data


# ----------------------------------------------------------------------------------------------------------- #
""" Encode, decode, convert """

def codec_name(codec):
    try:
        name = str(codec.name(), encoding='ascii')          # Python v3.
    except TypeError:
        name = str(codec.name())                            # Python v2.
    return name

# ----------------------------------------------------------------------------------------------------------- #
""" String """



# ----------------------------------------------------------------------------------------------------------- #
""" Math """

def get_all_odd(numLst):
    return [i for i in numLst if check_odd(i)]

def get_all_even(numLst):
    return [i for i in numLst if not check_odd(i)]

def resize_image(filename, desPth, w, h):
    with open(filename, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [w, h])
            cover.save(desPth, image.format)

# ----------------------------------------------------------------------------------------------------------- #
""" Clean up """

def del_key(key, dict = {}):
    try:
        del dict[key]
        print("configKey deleted: {key}".format(key=key))
    except KeyError:
        dict.pop(key, None)
        print("configKey poped: {key}".format(key=key))

def clean_file_ext(ext):
    fileNames = [f for f in get_file_path(os.getenv(__envKey__)) if f.endswith(ext)] or []
    if not fileNames == []:
        for filePth in fileNames:
            os.remove(filePth)

# - Naming ----
def clean_name(text):
    """
    Return a cleaned version of a string - removes everything
    but alphanumeric characters and dots.

    :param str text: string to clean.
    :returns: cleaned string.
    :rtype: str
    """
    return re.sub(r'[^a-zA-Z0-9\n\.]', '_', text)

def camel_case_to_title(text):
    """
    Split string by upper case letters and return a nice name.

    :param str text: string to convert.
    :returns: formatted string.
    :rtype: str
    """
    words = []
    from_char_position = 0
    for current_char_position, char in enumerate(text):
        if char.isupper() and from_char_position < current_char_position:
            words.append(text[from_char_position:current_char_position].title())
            from_char_position = current_char_position
    words.append(text[from_char_position:].title())
    return ' '.join(words)

def lower_case_underscore_to_camel_case(text):
    """
    Convert string or unicode from lower-case underscore to camel-case.

    :param str text: string to convert.
    :returns: formatted string.
    :rtype: str
    """
    split_string = text.split('_')
    # use string's class to work on the string to keep its type
    class_ = text.__class__
    return split_string[0] + class_.join('', map(class_.capitalize, split_string[1:]))


def autoRename(filename):
    # rename filename if already exists
    name, ext = os.path.splitext(filename)
    i = 0
    while 1:
        if not os.path.exists(filename) : return filename
        i+=1
        filename = name + str(i) + ext






# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 3:58 AM
# Pipeline manager - DAMGteam