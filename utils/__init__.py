#!/usr/bin/env python3
# coding=utf-8
"""
Script Name: utils.py
Author: Do Trinh/Jimmy - 3D artist.
Description:
    Here is where a lot of function need to use multiple times overall
"""
# -------------------------------------------------------------------------------------------------------------
from __future__ import absolute_import, unicode_literals
""" Import """

# Python
import os, sys, platform, subprocess, winshell
import requests, yaml, json, linecache, re
import datetime, time, uuid, win32api, pprint

from functools import WRAPPER_ASSIGNMENTS, WRAPPER_UPDATES, update_wrapper as _update_wrapper, partial


# PyQt5
from PyQt5.QtCore   import Qt, QRectF, QRect, QSize
from PyQt5.QtGui    import QColor, QFont, QFontMetrics

# PLM
from app  import __envKey__, __pkgsReq__, LOGO_DIR, WEB_ICON_DIR, TAG_DIR, AVATAR_DIR, KEYPACKAGE
from core.Handlers import IsADirectoryError, FileNotFoundError
from core.Loggers   import Loggers

logger = Loggers(__name__)
report = logger.report

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
            report("ERROR: (Incorrect Command) Valid commands are 'HIDE' and 'UNHIDE' (both are not case sensitive)")
    else:
        report("ERROR: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")

def batch_obj_properties_setting(listObj, mode):

    for obj in listObj:
        if os.path.exists(obj):
            obj_properties_setting(obj, mode)
        else:
            report('Could not find the specific path: %s' % obj)

# -------------------------------------------------------------------------------------------------------------
""" Error handle """

def handle_path_error(directory=None):
    if not os.path.exists(directory) or directory is None:
        try:
            raise IsADirectoryError("Path is not exists: {directory}".format(directory=directory))
        except IsADirectoryError as error:
            raise('Caught error: ' + repr(error))

def raise_exception():

    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)

    report("--------------------------------------------------------------------------------- \n"
            "Tracking from:   {0} \n"
            "At line number:  {1} \n"
            "Details code:    {2} \n"
            "{3} \n"
            "---------------------------------------------------------------------------------".format(os.path.basename(filename), lineno, line.strip(), exc_obj))
    return

def print_variable(varName, varData):
    print('###-------------------------------------------------------------------------------###')
    print('-------- CHECK VARIABLE: {0}'.format(varName))
    print('------------ File location: {0}'.format(__file__))
    print('------------ Variable type: {0}'.format(type(varName)))
    print(' ')
    print('-------- VARIABLE CONTENT')
    print(' ')

    pprint.pprint(varData)

    print(' ')
    print('-------- END CHECK')
    print('###-------------------------------------------------------------------------------###')

# -------------------------------------------------------------------------------------------------------------
""" Python """

def install_py_packages(name):
    """
    Install python package via command prompt
    :param name: name of component
    :return:
    """
    # report('Using pip to install %s' % name)
    if os.path.exists(name):
        subprocess.Popen('python %s install' % name)
    else:
        subprocess.Popen('python -m pip install %s' % name, shell=True).wait()

def install_require_package(package=__pkgsReq__):
    try:
        import package
    except ImportError as err:
        report("installing {0}".format(package))
        command = "start python -m pip install {0}".format(package)
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        status = p.wait()
        report("Command output: {0}".format(output))

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
            report('install new environment variable')
            os.environ[key] = path
    except KeyError:
        report('install new environment variable')
        os.environ[key] = path
    else:
        pass

# -------------------------------------------------------------------------------------------------------------
""" Command Prompt """

def cmd_execute_py(name, path):
    """
    Executing a python file
    :param name: python file name
    :param path: path to python file
    :return: executing in command prompt
    """
    report("Executing {name} from {path}".format(name=name, path=path))
    pth = os.path.join(path, name)
    if os.path.exists(pth):
        subprocess.call([sys.executable, pth])

def system_call(args, cwd="."):
    report("Running '{}' in '{}'".format(str(args), cwd))
    subprocess.call(args, cwd=cwd)
    pass

def run_cmd(pth):
    subprocess.Popen(pth)

def open_cmd():
    os.system("start /wait cmd")

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
            filePths.append(os.path.join(root, filename))  # Add to file list.
        for folder in directories:
            dirPths.append(os.path.join(root, folder)) # Add to folder list.
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

def get_app_icon(size=32, iconName="AboutPlt"):
    iconPth = os.path.join(os.getenv(__envKey__), 'imgs', 'icons', "x" + str(size))
    return os.path.join(iconPth, iconName + ".icon.png")

def get_logo_icon(size=32, name="DAMG"):
    if name == "Logo":
        logoPth = os.path.join(LOGO_DIR, 'Plm', 'icons')
    elif name == 'DAMG':
        logoPth = os.path.join(LOGO_DIR, 'DAMGteam', 'icons')
    else:
        logoPth = os.path.join(LOGO_DIR, 'Plt', 'icons')
    return os.path.join(logoPth, str(size) + "x" + str(size) + ".png")

def get_web_icon(name):
    icons = [i for i in get_file_path(WEB_ICON_DIR) if ".icon" in i]
    for i in icons:
        if name in i:
            return i

def get_avatar_icon(name):
    avatars = [a for a in get_file_path(AVATAR_DIR) if '.avatar' in a]
    for a in avatars:
        if name in a:
            return a

def get_tag_icon(name):
    tags = [t for t in get_file_path(TAG_DIR) if '.tag' in t]
    for t in tags:
        if name in t:
            return t

def generate_alternative_color(color, av):
    lightness = color.lightness()
    mult = float(lightness)/255
    return mult

def convert_to_QColor(data=None, alternate=False, av=20):
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
        report('Color from configuration is not recognized : ', data)
        report('Can only be [R, G, B] or [R, G, B, A]')
        report('Using default color !')
        color = QColor(120, 120, 120)
        if alternate:
            color = QColor(120-av, 120-av, 120-av)
        return color

def get_pointer_bounding_box(pointerPos, bbSize):
    point = pointerPos
    mbbPos = point
    point.setX(point.x() - bbSize / 2)
    point.setY(point.y() - bbSize / 2)
    size = QSize(bbSize, bbSize)
    bb = QRect(mbbPos, size)
    bb = QRectF(bb)
    return bb

# -------------------------------------------------------------------------------------------------------------
""" Read, Write, Edit json/yaml/config info """

def data_handler(type='json', mode='r', filePath=None, data={}):
    info = {}
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

# ----------------------------------------------------------------------------------------------------------- #
""" Clean up """

def del_key(key, dict = {}):
    try:
        del dict[key]
        report("key deleted: {key}".format(key=key))
    except KeyError:
        dict.pop(key, None)
        report("key poped: {key}".format(key=key))

def clean_file_ext(ext):
    fileNames = [f for f in get_file_path(os.getenv(__envKey__)) if ext in f] or []
    if not fileNames == []:
        for filePth in fileNames:
            os.remove(filePth)


# ----------------------------------------------------------------------------------------------------------- #
""" Naming """

def clean_name(text):
    """

    Return a cleaned version of a string - removes everything
    but alphanumeric characters and dots.
    :param str text: string to clean.
    :returns: cleaned string.
    :rtype: str

    """
    return re.sub(r'[^a-zA-Z0-9\n\.]', '_', text)


def camel_case_to_lower_case_underscore(text):
    """

    Split string by upper case letters.
    F.e. useful to convert camel case strings to underscore separated ones.
    :param str text: string to convert.
    :returns: formatted string.
    :rtype: str

    """
    words = []
    from_char_position = 0

    for current_char_position, char in enumerate(text):

        if char.isupper() and from_char_position < text:
            words.append(s[from_char_position:current_char_position].lower())
            from_char_position = current_char_position

    words.append(text[from_char_position:].lower())
    return '_'.join(words)


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



# ----------------------------------------------------------------------------------------------------------- #
""" Attribute Functions """

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
    return type(s) in [str, unicode]


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


def nodeParse(node):
    t = node[u"type"]

    if t == u"Program":
        body = [parse(block) for block in node[u"body"]]

        return Program(body)

    elif t == u"VariableDeclaration":
        kind = node[u"kind"]
        declarations = [parse(declaration) for declaration in node[u"declarations"]]
        return VariableDeclaration(kind, declarations)

    elif t == u"VariableDeclarator":
        id = parse(node[u"id"])
        init = parse(node[u"init"])
        return VariableDeclarator(id, init)

    elif t == u"Identifier":
        return Identifier(node[u"name"])

    elif t == u"Literal":
        return Literal(node[u"value"])

    elif t == u"BinaryExpression":
        operator = node[u"operator"]
        left = parse(node[u"left"])
        right = parse(node[u"right"])
        return BinaryExpression(operator, left, right)
    else:
        raise ValueError("Invalid data structure.")

def update_wrapper(wrapper, wrapped, *args, **kwargs):
    """Update wrapper, also setting .__wrapped__."""
    wrapper = _update_wrapper(wrapper, wrapped, *args, **kwargs)
    wrapper.__wrapped__ = wrapped
    return wrapper


def wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES):
    """ Backport of Python 3.5 wraps that adds .__wrapped__. """
    return partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)

# ----------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------
# Created by panda on 24/08/2018 - 8:07 AM
# © 2017 - 2018 DAMGteam. All rights reserved