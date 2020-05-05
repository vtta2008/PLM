#!/usr/bin/env python3
# coding=utf-8
"""
Script Name: utils.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    Here is where a lot of function need to use multiple times overall
"""
# -------------------------------------------------------------------------------------------------------------
from distutils.version import LooseVersion
""" Import """

# Python
import os, sys, platform, subprocess, winshell, yaml, json, re, linecache

from PIL                import Image
from resizeimage        import resizeimage

# PyQt5
from PyQt5.QtCore       import pyqtSignal, pyqtSlot, qVersion
from PyQt5.QtGui        import QKeySequence

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

def obj_properties_setting(directory, mode):
    if platform.system() == "Windows" or platform.system() == "Darwin":
        if mode == "h":
            if platform.system() == "Windows":
                subprocess.call(["attrib", "+H", directory])
            elif platform.system() == "Darwin":
                subprocess.call(["chflags", "hidden", directory])
        elif mode == "s":
            if platform.system() == "Windows":
                subprocess.call(["attrib", "-H", directory])
            elif platform.system() == "Darwin":
                subprocess.call(["chflags", "nohidden", directory])
        else:
            print("ERROR: (Incorrect Command) Valid commands are 'HIDE' and 'UNHIDE' (both are not case sensitive)")
    else:
        print("ERROR: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")

def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root,d) for d in dirs]:
            os.chmod(dir, mode)
    for file in [os.path.join(root, f) for f in files]:
            os.chmod(file, mode)

def batch_obj_properties_setting(listObj, mode):

    for obj in listObj:
        if os.path.exists(obj):
            obj_properties_setting(obj, mode)
        else:
            print('Could not find the specific path: %s' % obj)

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
""" Python """

def install_py_packages(name):
    """
    Install python package via command prompt
    :param name: name of component
    :return:
    """
    # print('Using pip to install %s' % name)
    if os.path.exists(name):
        subprocess.Popen('python %s install' % name)
    else:
        subprocess.Popen('python -m pip install %s' % name, shell=True).wait()

def install_require_package(package=__pkgsReq__):
    try:
        import package
    except ImportError as err:
        print("installing {0}".format(package))
        command = "start python -m pip install {0}".format(package)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        status = p.wait()
        print("Command output: {0}".format(output))

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

def get_py_env_var(key, path):
    try:
        pth = os.getenv(key)
        if pth == None or pth == '':
            print('install showLayout_new environment variable')
            os.environ[key] = path
    except KeyError:
        print('install showLayout_new environment variable')
        os.environ[key] = path
    else:
        pass

# -------------------------------------------------------------------------------------------------------------
""" Command Prompt """

def cmd_execute_py(name, directory):
    """
    Executing a python file
    :param name: python file name
    :param directory: path to python file
    :return: executing in command prompt
    """
    print("Executing {name} from {path}".format(name=name, path=directory))
    pth = os.path.join(directory, name)
    if os.path.exists(pth):
        return subprocess.call([sys.executable, pth])
    else:
        print("Path: {} does not exist".format(directory))

def system_call(args, cwd="."):
    print("Running '{}' in '{}'".format(str(args), cwd))
    return subprocess.call(args, cwd=cwd)

def run_cmd(pth):
    return subprocess.Popen(pth)

def open_cmd():
    return os.system("start /wait cmd")

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

def check_blank(data):
    if len(data) == 0 or data == "" or data is None:
        return False
    else:
        return True

def check_match(data1, data2):
    check = []
    if len(data1) == len(data2):
        for i in range(len(data1)):
            if data1[i] is data2[i]:
                continue
            else:
                check.append('False')
    else:
        check.append('False')

    if len(check) == 0:
        return True
    else:
        return False

# ----------------------------------------------------------------------------------------------------------- #
""" Math """

def check_odd(num):
    return str2bool(num%2)

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

def check_preset(data):
    if data == {}:
        pass
    else:
        return True

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

# - Attribute Functions ----
def auto_convert(value):
    """
    Auto-convert a value to it's given type.
    """
    atype = attr_type(value)
    if atype == 'str':
        return str(value)

    if atype == 'bool':
        return bool(value)

    if atype == 'float':
        return float(value)

    if atype == 'int':
        return int(value)
    return value




def is_newer(file1, file2):
    """
    Returns true if file1 is newer than file2.

    :param str file1: first file to compare.
    :param str file2: second file to compare.

    :returns: file1 is newer.
    :rtype: bool
    """
    if not os.path.exists(file1) or not os.path.exists(file2):
        return False

    time1 = os.path.getmtime(file1)
    time2 = os.path.getmtime(file2)
    return time1 > time2

def _loadConfig(filePath):
    with open(filePath, 'r') as myfile:
        fileString = myfile.read()
        cleanString = re.sub('//.*?\n|/\*.*?\*/', '', fileString, re.S)
        data = json.loads(cleanString)
    return data

def _saveData(filePath, data):
    f = open(filePath, "w")
    f.write(json.dumps(data,
                       sort_keys = True,
                       indent = 4,
                       ensure_ascii=False))
    f.close()
    print("Data successfully saved !")

def _loadData(filePath):
    with open(filePath) as json_file:
        j_data = json.load(json_file)
    json_file.close()
    print("Data successfully loaded !")
    return j_data

def _swapListIndices(inputList, oldIndex, newIndex):
    if oldIndex == -1:
        oldIndex = len(inputList)-1
    if newIndex == -1:
        newIndex = len(inputList)
    value = inputList[oldIndex]
    inputList.pop(oldIndex)
    inputList.insert(newIndex, value)

def setup_context_menu(graph):
    """
    Sets up the node graphs context menu with some basic menus and commands.
    .. code-block:: python
        :linenos:
        from NodeGraphQt import NodeGraph, setup_context_menu
        graph = NodeGraph()
        setup_context_menu(graph)
    Args:
        graph (NodeGraphQt.NodeGraph): node graph.
    """
    root_menu = graph.get_context_menu('graph')

    file_menu = root_menu.add_menu('&File')
    edit_menu = root_menu.add_menu('&Edit')

    # create "File" menu.
    file_menu.add_command('Open...', _open_session, QKeySequence.Open)
    file_menu.add_command('Save...', _save_session, QKeySequence.Save)
    file_menu.add_command('Save As...', _save_session_as, 'Ctrl+Shift+s')
    file_menu.add_command('Clear', _clear_session)

    file_menu.add_separator()

    file_menu.add_command('Zoom In', _zoom_in, '=')
    file_menu.add_command('Zoom Out', _zoom_out, '-')
    file_menu.add_command('Reset Zoom', _reset_zoom, 'h')

    # create "Edit" menu.
    undo_actn = graph.undo_stack().createUndoAction(graph.viewer(), '&Undo')
    if LooseVersion(qVersion()) >= LooseVersion('5.10'):
        undo_actn.setShortcutVisibleInContextMenu(True)
    undo_actn.setShortcuts(QKeySequence.Undo)
    edit_menu.qmenu.addAction(undo_actn)

    redo_actn = graph.undo_stack().createRedoAction(graph.viewer(), '&Redo')
    if LooseVersion(qVersion()) >= LooseVersion('5.10'):
        redo_actn.setShortcutVisibleInContextMenu(True)
    redo_actn.setShortcuts(QKeySequence.Redo)
    edit_menu.qmenu.addAction(redo_actn)

    edit_menu.add_separator()
    edit_menu.add_command('Clear Undo History', _clear_undo)
    edit_menu.add_separator()

    edit_menu.add_command('Copy', _copy_nodes, QKeySequence.Copy)
    edit_menu.add_command('Paste', _paste_nodes, QKeySequence.Paste)
    edit_menu.add_command('Delete', _delete_nodes, QKeySequence.Delete)

    edit_menu.add_separator()

    edit_menu.add_command('Select all', _select_all_nodes, 'Ctrl+A')
    edit_menu.add_command('Deselect all', _clear_node_selection, 'Ctrl+Shift+A')
    edit_menu.add_command('Enable/Disable', _disable_nodes, 'd')

    edit_menu.add_command('Duplicate', _duplicate_nodes, 'Alt+c')
    edit_menu.add_command('Center Selection', _fit_to_selection, 'f')

    edit_menu.add_separator()


# --- menu command functions. ---


def _zoom_in(graph):
    """
    Set the node graph to zoom in by 0.1
    Args:
        graph (NodeGraphQt.NodeGraph): node graph.
    """
    zoom = graph.get_zoom() + 0.1
    graph.set_zoom(zoom)


def _zoom_out(graph):
    """
    Set the node graph to zoom in by 0.1
    Args:
        graph (NodeGraphQt.NodeGraph): node graph.
    """
    zoom = graph.get_zoom() - 0.2
    graph.set_zoom(zoom)


def _reset_zoom(graph):
    graph.reset_zoom()


def _open_session(graph):
    """
    Prompts a file open dialog to load a session.
    Args:
        graph (NodeGraphQt.NodeGraph): node graph.
    """
    current = graph.current_session()
    viewer = graph.viewer()
    file_path = viewer.load_dialog(current)
    if file_path:
        graph.load_session(file_path)


def _save_session(graph):
    """
    Prompts a file save dialog to serialize a session if required.
    Args:
        graph (NodeGraphQt.NodeGraph): node graph.
    """
    current = graph.current_session()
    if current:
        graph.save_session(current)
        msg = 'Session layout saved:\n{}'.format(current)
        viewer = graph.viewer()
        viewer.message_dialog(msg, title='Session Saved')
    else:
        _save_session_as(graph)


def _save_session_as(graph):
    """
    Prompts a file save dialog to serialize a session.
    Args:
        graph (NodeGraphQt.NodeGraph): node graph.
    """
    current = graph.current_session()
    viewer = graph.viewer()
    file_path = viewer.save_dialog(current)
    if file_path:
        graph.save_session(file_path)


def _clear_session(graph):
    """
    Prompts a warning dialog to clear the node graph session.
    Args:
        graph (NodeGraphQt.NodeGraph): node graph.
    """
    viewer = graph.viewer()
    if viewer.question_dialog('Clear Current Session?', 'Clear Session'):
        graph.clear_session()


def _clear_undo(graph):
    """
    Prompts a warning dialog to clear undo.
    Args:
        graph (NodeGraphQt.NodeGraph): node graph.
    """
    viewer = graph.viewer()
    msg = 'Clear all undo history, Are you sure?'
    if viewer.question_dialog('Clear Undo History', msg):
        graph.undo_stack().clear()


def _copy_nodes(graph):
    graph.copy_nodes()


def _paste_nodes(graph):
    graph.paste_nodes()


def _delete_nodes(graph):
    graph.delete_nodes(graph.selected_nodes())


def _select_all_nodes(graph):
    graph.select_all()


def _clear_node_selection(graph):
    graph.clear_selection()


def _disable_nodes(graph):
    graph.disable_nodes(graph.selected_nodes())


def _duplicate_nodes(graph):
    graph.duplicate_nodes(graph.selected_nodes())


def _fit_to_selection(graph):
    graph.fit_to_selection()

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 3/06/2018 - 3:58 AM
# Pipeline manager - DAMGteam