#!/usr/bin/env python3
# coding=utf-8
"""
Script Name: utils.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    Here is where a lot of function need to use multiple times overall
"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import
from distutils.version import LooseVersion
""" Import """

# Python
import os, sys, requests, platform, subprocess, winshell, yaml, json, re, datetime, time, uuid, win32api, linecache

from PIL                import Image
from resizeimage        import resizeimage
from psutil             import cpu_percent, virtual_memory, disk_usage
from GPUtil             import getGPUs

# PyQt5
from PyQt5.QtCore       import Qt, QRectF, QRect, QSize, pyqtSignal, pyqtSlot, qVersion
from PyQt5.QtGui        import QColor, QFont, QFontMetrics, QKeySequence
from PyQt5.QtWidgets    import QAction, QPushButton

# PLM
from appData            import (__envKey__, __pkgsReq__, KEYPACKAGE, LOGO_DIR, WEB_ICON_DIR, TAG_ICON_DIR, AVATAR_DIR,
                                ICON_DIR, actionTypes)

# -------------------------------------------------------------------------------------------------------------
""" Destop tool """

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

def get_cpu_useage(interval=1, percpu=False):
    return cpu_percent(interval, percpu)

def get_ram_total():
    return byte2gigabyte(virtual_memory()[0])

def get_ram_useage():
    return virtual_memory()[2]

def get_gpu_total():
    gpus = getGPUs()
    total = 0.0
    for gpu in gpus:
        total += float(gpu.memoryTotal)
    return megabyte2gigabyte(total)

def get_gpu_useage():
    gpus = getGPUs()
    used = 0.0
    for gpu in gpus:
        used += float(gpu.memoryUsed/gpu.memoryTotal*100)
    rate = used/len(gpus)
    return round(rate, 2)

def get_disk_total():
    disk = disk_usage('/')
    return round(disk.total/(1024**3))

def get_disk_used():
    disk = disk_usage('/')
    return round(disk.used/(1024**3))

def get_disk_free():
    disk = disk_usage('/')
    return round(disk.free/(1024**3))

def get_disk_useage():
    disk = disk_usage('/')
    return disk.percent

def get_app_icon(size=32, iconName="About"):
    # Get the right directory base on icon size
    iconPth = os.path.join(ICON_DIR, "x{0}".format(str(size)))

    # Get the icon file path
    iconFilePth = os.path.join(iconPth, "{0}.icon.png".format(iconName))

    # Check icon file path
    if not os.path.exists(iconFilePth):
        print('could not find: {0}, please try a gain'.format(iconFilePth))

    return iconFilePth

def get_logo_icon(size=32, name="DAMG"):
    if name == "PLM":
        logoPth = os.path.join(LOGO_DIR, 'PLM')
    elif name == 'DAMG':
        logoPth = os.path.join(LOGO_DIR, 'DAMGTEAM')
    else:
        logoPth = os.path.join(LOGO_DIR, 'PLM')

    logoFilePth = os.path.join(logoPth, "{0}x{0}.png".format(str(size)))

    if not os.path.exists(logoFilePth):
        return FileNotFoundError('{} not exists'.format(logoFilePth))
    else:
        return logoFilePth

def get_web_icon(name):
    icons = [i for i in get_file_path(WEB_ICON_DIR) if ".icon" in i]
    for i in icons:
        if name in i:
            # print(i, os.path.exists(i))
            return i

def get_avatar_image(name):
    avatars = [a for a in get_file_path(AVATAR_DIR) if '.avatar' in a]
    for a in avatars:
        if name in a:
            # print(a, os.path.exists(a))
            return a

def get_tag_icon(name):
    tags = [t for t in get_file_path(TAG_ICON_DIR) if '.icon' in t]
    for t in tags:
        if name in t:
            # print(t, os.path.exists(t))
            return t

def generate_alternative_color(color, av):
    lightness = color.lightness()
    mult = float(lightness)/255
    return mult

def _convert_to_QColor(data=None, alternate=False, av=20):
    if len(data) == 3:
        color = QColor(data[0], data[1], data[2])
        if alternate:
            mult = generate_alternative_color(color, av)
            color = QColor(max(0, data[0]-(av*mult)), max(0, data[1]-(av*mult)), max(0, data[2]-(av*mult)))
        return color
    elif len(data) == 4:
        color = QColor(data[0], data[1], data[2], data[3])
        if alternate:
            mult = generate_alternative_color(color, av)
            color = QColor(max(0, data[0]-(av*mult)), max(0, data[1]-(av*mult)), max(0, data[2]-(av*mult)), data[3])
        return color
    else:
        print('ColorNotRecognize: Can only be [R, G, B] or [R, G, B, A], Using default color !', data)
        color = QColor(120, 120, 120)
        if alternate:
            color = QColor(120-av, 120-av, 120-av)
        return color

def _get_pointer_bounding_box(pointerPos, bbSize):
    point = pointerPos
    mbbPos = point
    point.setX(point.x() - bbSize / 2)
    point.setY(point.y() - bbSize / 2)
    size = QSize(bbSize, bbSize)
    bb = QRect(mbbPos, size)
    bb = QRectF(bb)
    return bb

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

# -------------------------------------------------------------------------------------------------------------
""" Collecting info user """

def get_user_location():

    package = KEYPACKAGE
    pythonVersion = sys.version
    windowOS = platform.system()
    windowVersion = platform.version()

    sysOpts = package['sysOpts']
    cache = os.popen2("SYSTEMINFO")
    source = cache[1].read()

    sysInfo = {}

    sysInfo['python'] = pythonVersion
    sysInfo['os'] = windowOS + "|" + windowVersion
    sysInfo['pcUser'] = platform.node()
    sysInfo['operating system'] = platform.system() + "/" + platform.platform()
    sysInfo['python version'] = platform.python_version()

    values = {}

    for opt in sysOpts:
        values[opt] = [item.strip() for item in re.findall("%s:\w*(.*?)\n" % (opt), source, re.IGNORECASE)][0]
    for item in values:
        sysInfo[item] = values[item]

    return sysInfo

def get_screen_resolution():
    resW = win32api.GetSystemMetrics(0)
    resH = win32api.GetSystemMetrics(1)
    return resW, resH

def get_window_taskbar_size():
    resW, resH = get_screen_resolution()
    monitors = win32api.EnumDisplayMonitors()
    display1 = win32api.GetMonitorInfo(monitors[0][0])
    tbH = resH - display1['Work'][3]
    tbW = resW
    return tbW, tbH

def get_local_pc_info():
    r = requests.get('https://api.ipdata.co').json()
    info = dict()
    for key in r:
        k = (str(key))
        for c in ['ip', 'city', 'country_name']:
            if k == c:
                info[k] = str(r[key])
            else:
                info[k] = 'unknown'

    return info['ip'], info['city'], info['country_name']

def get_layout_size(layout):
    sizeW = layout.frameGeometry().width()
    sizeH = layout.frameGeometry().height()
    return sizeW, sizeH

def get_text_size(text, painter=None):
    if not painter:
        metrics = QFontMetrics(QFont())
    else:
        metrics = painter.fontMetrics()
    size = metrics.size(Qt.TextSingleLine, text)
    return size

# ----------------------------------------------------------------------------------------------------------- #
""" Encode, decode, convert """

def codec_name(codec):
    try:
        name = str(codec.name(), encoding='ascii')          # Python v3.
    except TypeError:
        name = str(codec.name())                            # Python v2.
    return name

def text_to_utf8(input):
    return input.encode('utf-8')

def text_to_hex(text):
    return ''.join(["%02X" % ord(x) for x in str(text)])

def hex_to_text(hex):
    bytes = []
    hexStr = ''.join(str(hex).split(" "))
    for i in range(0, len(hexStr), 2):
        bytes.append(chr(int(hexStr[i:i + 2], 16)))
    outPut = ''.join(bytes)
    return outPut

def str2bool(arg):
    return str(arg).lower() in ['true', 1, '1', 'ok', '2']

def bool2str(arg):
    if arg:
        return "True"
    else:
        return "False"

def byte2gigabyte(byte):
    return round(byte/1073741824)

def megabyte2gigabyte(megabyte):
    return round(megabyte/1024)

def get_datetime():
    datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
    return datetime_stamp

def getDate():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[0]

def getTime():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[1]

def getToken():
    return str(uuid.uuid4())

def getUnix():
    return (str(uuid.uuid4())).split('-')[-1]

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

def attr_type(value):
    """
    Determine the attribute type based on a value.
    Returns a string.

    For example:

        value = [2.1, 0.5]
        type = 'float2'

    :param value: attribute value.

    :returns: attribute type.
    :rtype: str
    """
    if is_none(value):
        return 'null'

    if is_list(value):
        return list_attr_types(value)

    else:
        if is_bool(value):
            return 'bool'

        if is_string(value):
            return 'str'

        if is_number(value):
            if type(value) is float:
                return 'float'

            if type(value) is int:
                return 'int'
    return 'unknown'

def list_attr_types(s):
    """
    Return a string type for the value.

    .. todo::
        - 'unknown' might need to be changed
        - we'll need a feature to convert valid int/str to floats
          ie:
            [eval(x) for x in s if type(x) in [str, unicode]]
    """
    if not is_list(s):
        return 'unknown'

    for typ in [str, int, float, bool]:
        if all(isinstance(n, typ) for n in s):
            return '%s%d' % (typ.__name__, len(s))

    if False not in list(set([is_number(x) for x in s])):
        return 'float%d' % len(s)
    return 'unknown'

def is_none(s):
    return type(s).__name__ == 'NoneType'

def is_string(s):
    return type(s) in [str]

def is_button(s):
    if type(s) in [QPushButton]:
        return True
    elif s.Type in actionTypes:
        return True
    else:
        return False

def is_action(s):
    if type(s) in [QAction]:
        return True
    elif s.Type in actionTypes:
        return True
    else:
        return False

def is_number(s):
    """
    Check if a string is a int/float
    """
    if is_bool(s):
        return False
    return isinstance(s, int) or isinstance(s, float)

def is_bool(s):
    """
    Returns true if the object is a boolean value.
    * Updated to support custom decoders.
    """
    return isinstance(s, bool) or str(s).lower() in ['true', 'false']

def is_list(s):
    """
    Returns true if the object is a list type.
    """
    return type(s) in [list, tuple]

def is_dict(s):
    """
    Returns true if the object is a dict type.
    """
    from collections import OrderedDict
    return type(s) in [dict, OrderedDict]

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