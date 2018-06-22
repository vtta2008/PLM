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
import os, sys, requests, platform, subprocess, winshell, yaml, json, pip, re, datetime, time, uuid, win32api

# Plt
from appData.config import logger
from appData import __envKey__, __pkgsReq__, LOGODIR, KEYPACKAGE, WEBICONDIR, TAGDIR, AVATARDIR

# -------------------------------------------------------------------------------------------------------------
""" Metadata """

def query_metadata(key):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join('appData', '__init__.py')
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ')
            if parts and parts[0] == key:
                return parts[-1].strip("'")
    assert 0, "'{0}' not found in '{1}'".format(key, module_path)

def get_datetime():
    datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
    return datetime_stamp

def get_date():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[0]

def get_time():
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[1]

def get_token():
    return str(uuid.uuid4())

def get_unix():
    return (str(uuid.uuid4())).split('-')[-1]

# -------------------------------------------------------------------------------------------------------------
""" Destop tool """

def create_shotcut(target, icon, shortcut, description):
    winshell.CreateShortcut(
        Path=os.path.join(winshell.desktop(), shortcut),
        Target=target,
        Icon=(icon, 0),
        Description=description
    )

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
            logger.debug("ERROR: (Incorrect Command) Valid commands are 'HIDE' and 'UNHIDE' (both are not case sensitive)")
    else:
        logger.debug("ERROR: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")

def batch_obj_properties_setting(listObj, mode):

    for obj in listObj:
        if os.path.exists(obj):
            obj_properties_setting(obj, mode)
        else:
            pass
            # logger.info('Could not find the specific path: %s' % obj)

# -------------------------------------------------------------------------------------------------------------
""" Error handle """

def handle_path_error(directory=None):
    if not os.path.exists(directory) or directory is None:
        try:
            raise IsADirectoryError("Path is not exists: {directory}".format(directory=directory))
        except IsADirectoryError as error:
            logger.info('Caught error: ' + repr(error))

# -------------------------------------------------------------------------------------------------------------
""" Python """

def install_py_packages(name):
    """
    Install python package via command prompt
    :param name: name of component
    :return:
    """
    # logger.info('Using pip to install %s' % name)
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
            # logger.info('install new environment variable')
            os.environ[key] = path
    except KeyError:
        # logger.info('install new environment variable')
        os.environ[key] = path
    else:
        pass

# -------------------------------------------------------------------------------------------------------------
""" Command Prompt """

def cmd_execute_py(name, path, *args):
    """
    Executing a python file
    :param name: python file name
    :param path: path to python file
    :return: executing in command prompt
    """
    # logger.info("Executing {name} from {path}".format(name=name, path=path))
    pth = os.path.join(path, name)
    if os.path.exists(pth):
        subprocess.call([sys.executable, pth])

def system_call(args, cwd="."):
    # logger.info("Running '{}' in '{}'".format(str(args), cwd))
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

def getAppIcon(size=32, iconName="AboutPlt"):
    iconPth = os.path.join(os.getenv(__envKey__), 'imgs', 'icons', "x" + str(size))
    return os.path.join(iconPth, iconName + ".icon.png")

def getLogo(size=32, name="DAMG"):
    if name == "Logo":
        logoPth = os.path.join(LOGODIR, 'Plm', 'icons')
    elif name == 'DAMG':
        logoPth = os.path.join(LOGODIR, 'DAMGteam', 'icons')
    else:
        logoPth = os.path.join(LOGODIR, 'Plt', 'icons')

    return os.path.join(logoPth, str(size) + "x" + str(size) + ".png")

def getWebIcon(name):
    icons = [i for i in get_file_path(WEBICONDIR) if ".icon" in i]
    for i in icons:
        if name in i:
            return i

def getAvatar(name):
    avatars = [a for a in get_file_path(AVATARDIR) if '.avatar' in a]
    for a in avatars:
        if name in a:
            return a

def getTag(name):
    tags = [t for t in get_file_path(TAGDIR) if '.tag' in t]
    for t in tags:
        if name in t:
            return t

# -------------------------------------------------------------------------------------------------------------
""" Read, Write, Edit json/yaml data """

def dataHandle(type='json', mode='r', filePath=None, data={}):
    """
    json and yaml: read, write, edit... etc
    """
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

# -------------------------------------------------------------------------------------------------------------
""" Collecting info user """

def get_local_pc():

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

def get_pc_location():
    r = requests.get('https://api.ipdata.co').json()

    for key in r:
        k = (str(key))
        if k == 'ip':
            ip = str(r[key])
        elif k == 'city':
            city = str(r[key])
        elif k == 'country_name':
            country = str(r[key])
        else:
            ip = city = country = 'unknown'

    return ip, city, country

# ----------------------------------------------------------------------------------------------------------- #
""" Encode, decode, convert """

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
        # logger.info("key deleted: {key}".format(key=key))
    except KeyError:
        dict.pop(key, None)
        # logger.info("key poped: {key}".format(key=key))

def clean_pyc_file(var):
    fileNames = [f for f in get_file_path(os.getenv(__envKey__)) if var in f] or []
    if not fileNames == []:
        for filePth in fileNames:
            os.remove(filePth)


# ----------------------------------------------------------------------------------------------------------- #