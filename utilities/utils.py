#!/usr/bin/env python3
# coding=utf-8
"""
Script Name: utils.py
Author: Do Trinh/Jimmy - 3D artist.

Description:
    Here is where a lot of function need to use multiple times overall
"""
# -------------------------------------------------------------------------------------------------------------
""" Check data flowing """
# print("Import from modules: {file}".format(file=__name__))
# print("Directory: {path}".format(path=__file__.split(__name__)[0]))
# -------------------------------------------------------------------------------------------------------------
""" Import """

# Python
import os, sys, requests, logging, platform, shutil, subprocess, urllib, winshell, yaml, json, pip, re
import datetime, time, uuid, win32gui, win32api, pprint, cv2, socket, signal

from pyunpack import Archive

# Plt tools
import appData as app
from utilities import variables as var
from ui import WebBrowser

# -------------------------------------------------------------------------------------------------------------
""" Configure the current level to make it disable certain logs """
logPth = os.path.join(os.getenv(app.__envKey__), 'appData', 'logs', 'func.log')
logger = logging.getLogger(__name__)
handler = logging.FileHandler(logPth)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# ----------------------------------------------------------------------------------------------------------- #
""" Preset """

def preset_maya_intergrate(*args):
    # Pipeline tool module paths for Maya.
    maya_tk = os.path.join(os.getenv(app.__envKey__), 'packages', 'maya')

    # Name of folders
    mayaTrack = ['plt_modules', 'plugins', 'plt_anim', 'MayaLib', 'plt_model', 'plt_rig', 'plt_surface']
    pythonValue = ""
    pythonList = []
    for root, dirs, files in os.walk(maya_tk):
        for dir in dirs:
            if dir in mayaTrack:
                dirPth = os.path.join(root, dir)
                pythonList.append(dirPth)
    pythonList = list(set(pythonList))
    for pth in pythonList:
        pythonValue += pth + ';'
    os.environ['PYTHONPATH'] = pythonValue

    # Copy userSetup.py from source code to properly maya folder
    userSetup_plt_path = os.path.join(os.getenv(app.__envKey__), 'packages', 'maya', 'userSetup.py')
    userSetup_maya_path = os.path.join(os.path.expanduser('~/Documents/maya/2017/prefs/scripts'), 'userSetup.py')

    if not os.path.exists(userSetup_plt_path) or not os.path.exists(userSetup_plt_path):
        pass
    else:
        shutil.copy2(userSetup_plt_path, userSetup_maya_path)

def preset_load_appInfo(*args):
    """
    Load installed app info from config file
    :return: appInfo
    """
    # Seeking config file
    Collect_info()
    # Configure root path
    mainConfigPth = os.path.join(app.CONFIGPTH, 'main.yml')
    # Load info from file
    with open(mainConfigPth, 'r') as f:
        appInfo = yaml.load(f)

    return appInfo

def preset_load_iconInfo(*args):
    iconConfigPth = os.path.join(app.CONFIGPTH, 'icon.yml')
    with open(iconConfigPth, 'r') as f:
        iconInfo = yaml.load(f)
    return iconInfo

def preset_load_pyuiInfor(*args):
    pyuiConfigPth = os.path.join(app.CONFIGPTH, 'pyui.yml')
    with open(pyuiConfigPth, 'r') as f:
        pyuiInfo = yaml.load(f)
    return pyuiInfo

# -------------------------------------------------------------------------------------------------------------
""" Metadata """

def read_package_variable(key):
    """Read the value of a variable from the package without importing."""
    module_path = os.path.join('appData', '__init__.py')
    with open(module_path) as module:
        for line in module:
            parts = line.strip().split(' ')
            if parts and parts[0] == key:
                return parts[-1].strip("'")
    assert 0, "'{0}' not found in '{1}'".format(key, module_path)

# -------------------------------------------------------------------------------------------------------------
""" Error handle """

def handle_path_error(directory=None):
    if not os.path.exists(directory) or directory is None:
        try:
            raise IsADirectoryError("Path is not exists: {directory}".format(directory=directory))
        except IsADirectoryError as error:
            logger.debug('Caught error: ' + repr(error))

def mark_tracking_data(data):
    pprint.pprint(var.LLINE)
    pprint.pprint(data)
    pprint.pprint(var.LLINE)
    pprint.pprint("Modules {name}: Marked".format(name=os.path.basename(__file__)))
    pprint.pprint(__file__)
    sys.exit()

# -------------------------------------------------------------------------------------------------------------
""" Installation """

def install_py_packages(name, *args):
    """
    Install python package via command prompt
    :param name: name of component
    :return:
    """
    logger.info('Using pip to install %s' % name)
    if os.path.exists(name):
        subprocess.Popen('python %s install' % name)
    else:
        subprocess.Popen('python -m pip install %s' % name, shell=True).wait()

def install_required_package():
    for pkg in app.__pkgsReq__:
        try:
            subprocess.Popen("python -m pip install %s" % pkg)
        except FileNotFoundError:
            subprocess.Popen("pip install %s" % pkg)
        finally:
            subprocess.Popen("python -m pip install --upgrade %s" % pkg)

def uninstall_all_required_package():
    __pkgsReq__ = app.__pkgsReq__
    for pkg in app.__pkgsReq__:
        try:
            subprocess.Popen("python -m pip uninstall %s" % pkg)
        except FileNotFoundError:
            subprocess.Popen("pip uninstall %s" % pkg)
            __pkgsReq__.remove(pkg)

    if len(__pkgsReq__)==0:
        return True
    else:
        return False

# -------------------------------------------------------------------------------------------------------------
""" Inspect info """

def get_python_pkgs():
    pyPkgs = {}
    pyPkgs['__mynote__'] = 'import pip; pip.get_installed_distributions()'

    for package in pip.get_installed_distributions():
        name = package.project_name  # SQLAlchemy, Django, Flask-OAuthlib
        key = package.key  # sqlalchemy, django, flask-oauthlib
        module_name = package._get_metadata("top_level.txt")  # sqlalchemy, django, flask_oauthlib
        location = package.location  # virtualenv lib directory etc.
        version = package.version  # version number

        pyPkgs[name] = [key, version, location]

    pkgConfig = os.path.join(os.getenv(app.__envKey__), 'appData', 'pkgs_config.yml')

    with open(pkgConfig, 'w') as f:
        yaml.dump(pyPkgs, f, default_flow_style=False)

    return pyPkgs

def inspect_package(name):
    """
    check python component, if false, it will install component
    :param name:
    :return:
    """
    # logger.info( 'Trying to import %s' % name )
    allPkgs = get_python_pkgs()
    if name in allPkgs:
        # logger.info('package "%s" is already installed' % name)
        pass
    else:
        logger.info('package "%s" is not installed, '
                    'execute package installation procedural' % name)
        install_py_packages(name)

def get_all_env_key(key, path):
    try:
        pth = os.getenv(key)
        if pth == None or pth == '':
            logger.info('install new environment variable')
            os.environ[key] = path
    except KeyError:
        logger.info('install new environment variable')
        os.environ[key] = path
    else:
        pass

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

# -------------------------------------------------------------------------------------------------------------
""" Functions content """

def download_single_file(url, path_to, *args):
    execute_download = urllib.urlretrieve(url, path_to)
    logger.info(execute_download)
    logger.info("Downloaded to: %s" % str(path_to))

def download_image_from_url(link, *args):
    fileName = os.path.basename(link)
    imgPth = os.path.join(os.getenv(app.__envKey__), 'avatar')
    avatarPth = os.path.join(imgPth, fileName)

    if not os.path.exists(avatarPth):
        download_single_file(link, avatarPth)

    return avatarPth

def extract_files(inDir, file_name, outDir, *args):
    Archive(os.path.join(inDir, file_name)).extractall(outDir)

def fix_image_files(root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for dir in dirs:
            system_call("mogrify *.png", "{}".format(os.path.join(path, dir)))

def obj_properties_setting(directory, mode, *args):
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
            logger.error("ERROR: (Incorrect Command) Valid commands are 'HIDE' and 'UNHIDE' (both are not case sensitive)")
    else:
        logger.error("ERROR: (Unknown Operating System) Only Windows and Darwin(Mac) are Supported")

def batch_obj_properties_setting(listObj, mode, *args):

    for obj in listObj:
        if os.path.exists(obj):
            obj_properties_setting(obj, mode)
        else:
            logger.info('Could not find the specific path: %s' % obj)

def clean_unnecessary_file(var, *args):
    fileNames = [f for f in get_file_path(os.getenv(app.__envKey__)) if var in f] or []
    if not fileNames == []:
        for filePth in fileNames:
            os.remove(filePth)

def batch_resize_image(imgDir=None, imgResDir=None, size=[100, 100], sub=False, ext='.png', mode=1):
    """
    resize multiple images at once
    :param imgDir: the path of images will be resized
    :param imgResDir: the path to store images after resizing
    :param size: how big or small images will be resized

    """
    if imgDir == None:
        sys.exit()

    if not os.path.exists(imgDir):
        logger.info('The source folder: %s is not exists' % imgDir)
        sys.exit()

    if imgResDir == None:
        imgResDir = imgDir

    if not os.path.exists(imgResDir):
        os.mkdir(imgResDir)

    if not sub:
        images = [i for i in os.listdir(imgDir) if i.endswith(ext)]
    else:
        filePths = get_file_path(imgDir)
        images = [os.path.abspath(i) for i in filePths if i.endswith(ext)]

    resized_images = []

    for image in images:
        imgPth = os.path.join(imgDir, image)
        resizedName = 'resized_%s' % image
        resDir = os.path.join(imgResDir, resizedName)
        img = cv2.imread(imgPth, mode)
        resized_image = cv2.resize(img, (size[0], size[1]))
        cv2.imwrite(resDir, resized_image)

        resized_images.append(resDir)

    return images, resized_images

def resize_image(imgPthSrc, imgPthDes, size=[100,100]):

    img = cv2.imread(imgPthSrc, 1)
    resized_image = cv2.resize(img, (size[0], size[1]))
    cv2.imwrite(imgPthDes, resized_image)

def dataHandle(type='json', mode='r', filePath=None, data={}, *args):
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

def cmd_execute_py(name, path, *args):
    """
    Executing a python file
    :param name: python file name
    :param path: path to python file
    :return: executing in command prompt
    """
    logger.info("Executing {name} from {path}".format(name=name, path=path))
    pth = os.path.join(path, name)
    if os.path.exists(pth):
        subprocess.call([sys.executable, pth])

def system_call(args, cwd="."):
    print("Running '{}' in '{}'".format(str(args), cwd))
    subprocess.call(args, cwd=cwd)
    pass

def send_udp(value, *args):
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.sendto(value, (app.UDP_IP, app.UDP_PORT))

def openWebsite(url, *args):
    web = WebBrowser.WebBrowser(url)
    web.show()
    web.exec_()

def show_hide_layout(key, *args):
    if key == "AboutPlt":
        from ui import AboutPlt
        layout = AboutPlt.AboutPlt()
    elif key == "Calculator":
        from ui import Calculator
        layout = Calculator.Calculator()
    elif key == "Calendar":
        from ui import Calendar
        layout = Calendar.Calendar()
    elif key == "EnglishDictionary":
        from ui import EnglishDictionary
        layout = EnglishDictionary.EnglishDictionary()
    elif key == "FindFiles":
        from ui import FindFiles
        layout = FindFiles.FindFiles()
    elif key == "ForgotPassword":
        from ui import ForgotPassword
        layout = ForgotPassword.ForgotPassword()
    elif key == "ImageViewer":
        from ui import ImageViewer
        layout = ImageViewer.ImageViewer()
    elif key == "InfoTemplate":
        from ui import AboutPlt
        layout = AboutPlt.AboutPlt()
    elif key == "NewProject":
        from ui import NewProject
        layout = NewProject.NewProject()
    elif key == "NoteReminder":
        from ui import NoteReminder
        layout = NoteReminder.NoteReminder()
    elif key == "Preference":
        from ui import Preference
        layout = Preference.Preference()
    elif key == "Screenshot":
        from ui import Screenshot
        layout = Screenshot.Screenshot()
    elif key == "SignIn":
        from ui import SignIn
        layout = SignIn.SignIn()
    elif key == "SignUp":
        from ui import SignUp
        layout = SignUp.SignUp()
    elif key == "TextEditor":
        from ui import TextEditor
        layout = TextEditor.TextEditor()
    elif key == "UserSetting":
        from ui import UserSetting
        layout = UserSetting.UserSetting()
    elif key == "WebBrowser":
        from ui import WebBrowser
        layout = WebBrowser.WebBrowser()

    print(4)
    # layout.show()
    print(5)
    layout.exec_()
    print(6)

def reconfig_data(*args):
    pass

def operate_function(funcName):
    if funcName == "clean_unnecessary_file":
        return clean_unnecessary_file(".pyc")
    elif funcName == "reconfig_data":
        return reconfig_data()

def openProcess(data, *args):
    if "Load python layout: " in data:
        return show_hide_layout(data.split("Load python layout: ")[-1])
    elif "Send UDP: " in data:
        return send_udp(data.split("Send UDP: ")[-1])
    elif data == "Exit programe":
        return sys.exit(1)
    elif "Open website: " in data:
        return openWebsite(data.split("Open website: ")[-1])
    elif "Use function: " in data:
        return operate_function(data.split("Use function: ")[-1])
    else:
        return subprocess.Popen(data)

# -------------------------------------------------------------------------------------------------------------
""" Collecting info user """

def get_local_pc(*args):

    package = var.PLT_PKG
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

def get_screen_resolution(*args):
    resW = win32api.GetSystemMetrics(0)
    resH = win32api.GetSystemMetrics(1)
    return resW, resH

def get_window_taskbar_size(*args):
    resW, resH = get_screen_resolution()
    monitors = win32api.EnumDisplayMonitors()
    display1 = win32api.GetMonitorInfo(monitors[0][0])
    tbH = resH - display1['Work'][3]
    tbW = resW
    return tbW, tbH

def get_datetime(*args):
    datetime_stamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y.%m.%d||%H:%M:%S'))
    return datetime_stamp

def get_date(*args):
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[0]

def get_time(*args):
    datetimeLog = get_datetime()
    return datetimeLog.split('||')[1]

def get_token(*args):
    return str(uuid.uuid4())

def get_unix(*args):
    return (str(uuid.uuid4())).split('-')[-1]

def get_title():
    import random
    secure_random = random.SystemRandom()
    value = secure_random.choice(var.USER_CLASS)
    return value

def get_pc_location(*args):
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

# -------------------------------------------------------------------------------------------------------------
""" Layout setting """

def set_buffer_and_offset(offsetX=5, offsetY=5, *args):
    tbW, tbH = get_window_taskbar_size()
    resW, resH = get_screen_resolution()
    if tbW == resW:
        bufferX = 0
    elif tbW > resW:
        bufferX = resW - tbW
    else:
        bufferX = tbW - resW
    bufferY = tbH
    return bufferX, bufferY, offsetX, offsetY

def set_app_stick_to_bot_right(sizeW=400, sizeH=280, offsetX=5, offsetY=5, *args):
    resW, resH = get_screen_resolution()
    bufferX, bufferY, offsetX, offsetY = set_buffer_and_offset(offsetX, offsetY)
    posX = resW - (sizeW + bufferX + offsetX)
    posY = resH - (sizeH + bufferY + offsetY)
    return posX, posY, sizeW, sizeH

def set_app_stick_to_bot_left(sizeW=400, sizeH=280, offsetX=5, offsetY=5, *args):
    resW, resH = get_screen_resolution()
    bufferX, bufferY, offsetX, offsetY = set_buffer_and_offset(offsetX, offsetY)
    posX = offsetX
    posY = resH - (sizeH + bufferY + offsetY)
    return posX, posY, sizeW, sizeH

def set_app_stick_to_top_right(sizeW=400, sizeH=280, offsetX=5, offsetY=5, *args):
    resW, resH = get_screen_resolution()
    bufferX, bufferY, offsetX, offsetY = set_buffer_and_offset(offsetX, offsetY)
    posX = resW - (sizeW + bufferX + offsetX)
    posY = offsetX + bufferY
    return posX, posY, sizeW, sizeH

def set_app_stick_to_top_left(sizeW=400, sizeH=280, offsetX=5, offsetY=5, *args):
    bufferX, bufferY, offsetX, offsetY = set_buffer_and_offset(offsetX, offsetY)
    posX = offsetX + bufferX
    posY = offsetY + bufferY
    return posX, posY, sizeW, sizeH

# ----------------------------------------------------------------------------------------------------------- #
""" Plt app functions """

def screenshot(*args):
    from ui import Screenshot
    screen = Screenshot.Screenshot()
    screen.exec_()

def open_app(pth, *args):
    subprocess.Popen(pth)

# ----------------------------------------------------------------------------------------------------------- #
""" Quick find path """

def get_icon(key, *args):
    iconConfig = os.path.join(os.getenv(app.__envKey__), 'appData', 'config', 'icon.json')
    with open(iconConfig, 'r') as f:
        iconInfo = json.load(f)
    for k in iconInfo:
        if key in k:
            return iconInfo[k]
    return "No Value"

def get_web_icon(key, *args):
    iconLst = get_file_path(os.path.join(os.getenv(app.__envKey__), 'imgs', 'web'))
    for icon in iconLst:
        if key in icon:
            return icon

def get_avatar(key, *args):
    avatarLst = [i for i in get_file_path(os.path.join(os.getenv(app.__envKey__), 'imgs', 'avatar')) if '.avatar' in i]
    for avatar in avatarLst:
        if key in avatar:
            return avatar

def get_tag(key, *args):
    tagLst = [i for i in get_file_path(os.path.join(os.getenv(app.__envKey__), 'imgs', 'tags')) if '.tag' in i]
    for tag in tagLst:
        if key in tagLst:
            return tag

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
""" Checking info """

def check_blank(data, *args):
    if len(data) == 0 or data == "" or data is None:
        return False
    else:
        return True

def check_match(data1, data2, *args):
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
""" Remove data """
def del_key(key, dict = {}):
    if not key in dict:
        logger.debug("key not exists: {key}".format(key=key))
        pass
    else:
        try:
            del dict[key]
            logger.debug("key deleted: {key}".format(key=key))
        except KeyError:
            dict.pop(key, None)
            logger.debug("key poped: {key}".format(key=key))

# ----------------------------------------------------------------------------------------------------------- #
""" Collecting all info. """

class Collect_info():
    """
    Initialize the main class functions
    :param package: the package of many information stored from default variable
    :param names: the dictionary of names stored from default variable
    :returns: all installed app info, package app info, icon info, image info, pc info.

    """
    def __init__(self):

        super(Collect_info, self).__init__()

        self.collect_env_variables()
        self.collect_icon_path()
        self.collect_pyui_path()
        self.collect_all_app()
        self.collect_main_app()

    def collect_env_variables(self):
        envKeys = {}
        for key in os.environ.keys():
            envKeys[key] = os.getenv(key)
        self.create_config_file('envKeys', envKeys)

    def collect_icon_path(self):
        """
        Get all the info of plt.maya.icon
        :param names: the dictionsary of names stored from default variable
        :return: plt.maya.icon.info
        """
        # Create dictionary for icon info
        self.iconInfo = {}
        self.iconInfo['Logo'] = os.path.join('imgs', 'Logo.icon.png')
        # Custom some info to debug
        self.iconInfo['Sep'] = 'separato.png'
        self.iconInfo['File'] = 'file.png'
        # Get list of icons in imgage folder
        iconlst = [i for i in get_file_path(os.path.join(os.getenv(app.__envKey__), 'imgs', 'main')) if '.icon' in i] \
                  + [i for i in get_file_path(os.path.join(os.getenv(app.__envKey__), 'imgs', 'apps')) if '.icon' in i] \
                  + [i for i in get_file_path(os.path.join(os.getenv(app.__envKey__), 'imgs', 'dev')) if '.icon' in i]
    
        for i in iconlst:
            self.iconInfo[os.path.basename(i).split('.icon')[0]] = i

        self.create_config_file('icon', self.iconInfo)

    def collect_all_app(self):
        """
        It will find and put all the info of installed apps to two list: appname and path
        :param filters: self.appName, self.appPath
        :return: self.appName, self.appPath
        """
        shortcuts = {}
        appName = []
        appPth = []

        all_programs = winshell.programs(common=1)

        for dirpath, dirnames, filenames in os.walk(all_programs):
            relpath = dirpath[1 + len(all_programs):]
            shortcuts.setdefault(relpath, []).extend([winshell.shortcut(os.path.join(dirpath, f)) for f in filenames])
        for relpath, lnks in sorted(shortcuts.items()):
            for lnk in lnks:
                name, _ = os.path.splitext(os.path.basename(lnk.lnk_filepath))
                appName.append(name)
                appPth.append(lnk.path)

        self.appInfo = {}
        for name in appName:
            self.appInfo[str(name)] = str(appPth[appName.index(name)])

        self.create_config_file("app", self.appInfo)

    def collect_pyui_path(self):
        self.pyToolInfor = {}
        for key in app.CONFIG_MAIN:
            pyPth = os.path.join(os.getenv(app.__envKey__), "ui", key + ".py")
            if os.path.exists(pyPth):
                self.pyToolInfor[key] = "Load python layout: {key}".format(key=key)
        self.create_config_file('pyui', self.pyToolInfor)

    def collect_main_app(self):

        self.mainInfo = {}

        detectLst = app.KEY_DETECT
        pltLst = app.KEY_PKGS

        delKeys = [k for k in self.appInfo if not self.appInfo[k].endswith('.exe')]

        for key in delKeys:
            del_key(key, self.appInfo)

        keepKeys = []
        for k in pltLst:
            for key in self.appInfo:
                if k in key:
                    keepKeys.append(key)
        delKeys = [k for k in self.appInfo if not k in keepKeys]
        for key in delKeys:
            del_key(key, self.appInfo)

        delKeys = []
        for key in self.appInfo:
            for k in detectLst:
                if k in key:
                    delKeys.append(key)
        for key in delKeys:
            del_key(key, self.appInfo)

        # Custom functions
        self.mainInfo['Logo'] = [app.__appname__, self.iconInfo['Logo'], ' ']
        self.mainInfo['Separator'] = ['separator', self.iconInfo['Sep'], ' ']
        self.mainInfo['File'] = ['File', self.iconInfo['File'], ' ']

        self.mainInfo['Exit'] = ['Exit Pipeline Tool', self.iconInfo['Exit'], '']

        self.mainInfo['About'] = ['About Plt', self.iconInfo['AboutPlt'], '']
        self.mainInfo['Credit'] = ['Credit', self.iconInfo['Credit'], '']
        self.mainInfo['Preferences'] = ['Preferences', self.iconInfo['Preferences'], '']

        self.mainInfo['Help'] = ['PLt wiki', self.iconInfo['Help'], '']

        self.mainInfo['CleanPyc'] = ['Clean ".pyc" files', self.iconInfo['CleanPyc'], '']
        self.mainInfo['ReConfig'] = ['Re configuring data', self.iconInfo['Reconfig'], '']

        self.mainInfo['Shutdown'] = ['Shut down your pc', self.iconInfo['Shutdown'], '']
        self.mainInfo['FM'] = ['FM radio', self.iconInfo['FM'], '']
        self.mainInfo['ViewSplit'] = ['View split left right', self.iconInfo['ViewSplit'], '']
        self.mainInfo['Mute'] = ['Mute your volume', self.iconInfo['Mute'], '']
        self.mainInfo['VolumeUp'] = ['Turn your volume up', self.iconInfo['VolumeUp'], '']
        self.mainInfo['VolumeDown'] = ['Turn your volume down', self.iconInfo['VolumeDown'], '']
        self.mainInfo['ChannelUp'] = ['Media skip forward', self.iconInfo['SkipForward'], '']
        self.mainInfo['ChannelDown'] = ['Media skip backward', self.iconInfo['SkipBackward'], '']


        # Fixing the path to open desire app.
        for key in self.appInfo:
            if 'NukeX' in key:
                logger.debug("key found: {key}, need to fix value".format(key=key))
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --nukex"
                logger.debug("Fixed: {key}: {val}".format(key=key, val=self.appInfo[key]))
            elif 'Hiero' in key:
                logger.debug("key found: {key}, need to fix value".format(key=key))
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " --hiero"
                logger.debug("Fixed: {key}: {val}".format(key=key, val=self.appInfo[key]))
            elif 'UVLayout' in key:
                logger.debug("key found: {key}, need to fix value".format(key=key))
                self.appInfo[key] = '"' + self.appInfo[key] + '"' + " -launch"
                logger.debug("Fixed: {key}: {val}".format(key=key, val=self.appInfo[key]))



        # Extra app come along with plt but not be installed in local.
        dbBrowserPth = os.path.join(os.getenv(app.__envKey__), 'external_app', 'sqlbrowser', 'SQLiteDatabaseBrowserPortable.exe')
        advanceRenamerPth = os.path.join(os.getenv(app.__envKey__), 'external_app', 'batchRenamer', 'ARen.exe')
        qtDesigner = os.path.join(os.getenv('PROGRAMDATA'), 'Anaconda3', 'Library', 'bin', 'designer.exe')
        davinciPth = os.path.join(os.getenv('PROGRAMFILES'), 'Blackmagic Design', 'DaVinci Resolve', 'resolve.exe')
        commandPromptPth = os.getenv('COMSPEC')

        eVal = [dbBrowserPth, advanceRenamerPth, qtDesigner, davinciPth, commandPromptPth]
        eKeys = ['Database Browser', 'Advance Renamer', 'QtDesigner', "Davinci Resolve", "Command Prompt"]

        for key in eKeys:
            if os.path.exists(eVal[eKeys.index(key)]):
                self.mainInfo[key] = [key, get_icon(key), eVal[eKeys.index(key)]]

        for key in self.appInfo:
            self.mainInfo[key] = [key, get_icon(key), self.appInfo[key]]

        for key in self.pyToolInfor:
            self.mainInfo[key] = [key, get_icon(key), self.pyToolInfor[key]]

        self.create_config_file('main', self.mainInfo)

    def create_config_file(self, name, data):
        appsConfig_yaml = os.path.join(os.getenv(app.__envKey__), 'appData', 'config', '{name}.yml'.format(name=name))
        appsConfig_json = os.path.join(os.getenv(app.__envKey__), 'appData', 'config', '{name}.json'.format(name=name))
        dataHandle('yaml', 'w', appsConfig_yaml, data)
        dataHandle('json', 'w', appsConfig_json, data)

# ----------------------------------------------------------------------------------------------------------- #